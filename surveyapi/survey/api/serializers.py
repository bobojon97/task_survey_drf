from rest_framework import serializers
from survey.models import Schema, Question, Survey

class SchemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schema
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = "__all__"

class SurveySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Survey
        fields = "__all__"