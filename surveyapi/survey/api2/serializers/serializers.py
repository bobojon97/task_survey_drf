from typing import Iterable, List
from rest_framework import serializers
from survey.models import *

def validate_options(question: Question, options: list):
    if question.answer_type == 'TEXT':
        if options:
            raise serializers.ValidationError('Answer options for the type "TEXT"')
    else:
        if (not isinstance(options, list)) or (len(options) < 2):
            raise serializers.ValidationError('Should be a list or more values')


class AnswerOptionSerializer(serializers.ModelSerializer):

    def to_representation(self, iterable):
        net = super().to_representation(iterable)
        return net['text']

    class Meta:
        model = AnswerOption
        fields = ['text']

class QuestionSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=False, max_length=255)
    answer_options = AnswerOptionSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answer_type']


class SchemeQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    def to_representation(self, iterable):
        ret = super().to_representation(iterable)
        return ret['question']

    class Meta:
        model = SchemaQuestion
        fields = ['question']

class SchemeSerializerMixin:
    question_model = Question
    questions_field = 'scheme_question'
    view_field = 'questions'

    def create(self, validated_data: dict):
        questions_data = validated_data.pop(self.view_field)
        instance = self.Meta.model.objects.create(**validated_data)
        self.add_questions(instance, questions_data)
        return instance

    def validate_date_to(self, value):
        start_data = getattr(self.instance, 'start_data', date.today())
        if value < start_data:
            raise serializers.ValidationError('Value "end_data" should not be earlier than "start_data"')
        return value

    def add_questions(self, instance: Schema, questions_data: Iterable[dict]):
        to_create = []
        for question_data in questions_data:
            data = question_data['question']
            options = data.pop('answer_options', [])
            question = Question(**data)
            question.save()
            self.add_options(question, options)

            sq = SchemaQuestion(scheme=instance, question=question)
            to_create.append(sq)

        if to_create:
            SchemaQuestion.objects.bulk_create(to_create)

    @staticmethod
    def add_options(question: Question, options: List[dict]):
        options_field = getattr(question, 'answer_options')
        current_options = options_field.all()
        if current_options:
            current_options.delete()

        validate_options(question, options)
        to_create = []
        for v in options:
            instance = AnswerOption(**v)
            instance.question = question
            to_create.append(instance)

        if to_create:
            instances = AnswerOption.objects.bulk_create(to_create)
            options_field.set(instances)

    def delete_questions(self, questions_data: Iterable[dict]):
        if questions_data:
            questions_ids = [i['question']['id'] for i in questions_data]
            self.question_model.objects.filter(id__in=questions_ids).delete()

    def update_questions(self, questions_data: Iterable[dict]):
        to_update, fields = [], []
        for data in questions_data:
            question_data = data['question']
            question = self.question_model.objects.select_for_update().get(id=question_data['id'])
            serializer = QuestionSerializer(data=question_data)
            if serializer.is_valid(raise_exception=True):
                for field, value in serializer.validated_data.items():
                    if field == 'id':
                        continue
                    elif field == 'answer_options':
                        self.add_options(question, value)
                    else:
                        setattr(question, field, value)
                        fields.append(field)
                to_update.append(question)

        if to_update and fields:
            self.question_model.objects.bulk_update(to_update, fields=fields)

    def update_scheme_with_questions(self, instance: Schema, questions_data: Iterable[dict]):
        data_to_delete = filter(
                lambda item: tuple(item['question'].keys()) == ('id',), questions_data
        )
        self.delete_questions(data_to_delete)

        def get_updating(item):
            keys = tuple(item['question'].keys())
            return 'id' in keys and keys != ('id',)

        data_update = filter(get_updating, questions_data)
        self.update_questions(data_update)

        newdata = filter(lambda item: item['question'].get('id') is None, questions_data)
        self.add_questions(instance, newdata)


class SchemeListSerializer(serializers.HyperlinkedModelSerializer, SchemeSerializerMixin):

    class Meta:
        model = Schema
        fields = ['id',  'name', 'description', 'start_data', 'end_data']


class SchemeSerializer(serializers.HyperlinkedModelSerializer, SchemeSerializerMixin):
    scheme_question = SchemeQuestionSerializer(many=True)

    def update(self, instance, validated_data):
        questions_data = validated_data.pop(self.questions_field, [])
        if questions_data:
            self.update_scheme_with_questions(instance, questions_data)
        instance = super().update(instance, validated_data)
        return instance

    def to_representation(self, iterable):
        ret = super().to_representation(iterable)
        ret[self.view_field] = ret.pop(self.questions_field)
        return ret

    class Meta:
        model = Schema
        fields = ['id',  'name', 'description', 'start_data', 'end_data']