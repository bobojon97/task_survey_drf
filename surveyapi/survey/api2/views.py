from django.shortcuts import redirect
from rest_framework import permissions, generics, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from survey.models import *
from survey.api2.serializers.serializers import *
from survey.api2.serializers.serializers2 import *
from survey.api2.generics import GetPatchAPIView

@api_view(['GET'])
def api2_root(request, format=None):
    return Response({
        'admin': {
            'schemas': reverse('scheme-list', request=request, format=format),
            'participants': reverse('participant-list', request=request, format=format),
        },
        'participant': reverse('survey-list', request=request, format=format),
    })
    
class ParticipantAPIViewMixin:
    queryset = Participant.objects.all()

class ParticipantListAPIView(ParticipantAPIViewMixin, generics.ListAPIView):
    serializer_class = ParticipantListSerializer
    permission_classes = [
        permissions.IsAdminUser
    ]


class ParticipantDetailAPIView(ParticipantAPIViewMixin):
    serializer_class = ParticipantDetailSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]


class SchemeAPIViewMixin:
    queryset = Schema.objects.all()
    permission_classes = [
        permissions.IsAdminUser
    ]

    def convert_request_data(self, request):
        view_field = self.serializer_class.view_field
        # todo: не через _mutable
        if not isinstance(request.data, dict):
            request.data._mutable = True
        questions = request.data.pop(view_field, [])
        for q in questions:
            options = q.get('answer_options')
            if options:
                if not isinstance(options, list):
                    raise serializers.ValidationError('Options should be a list')
                q['answer_options'] = [{'text': opt} for opt in options]

        field = self.serializer_class.questions_field
        request.data[field] = [{'question': q} for q in questions]
        return request


class SchemeListAPIView(SchemeAPIViewMixin, generics.ListCreateAPIView):
    serializer_class = SchemeListSerializer

    def create(self, request, *args, **kwargs):
        request = self.convert_request_data(request)
        return super().create(request, *args, **kwargs)


class SchemeDetailAPIView(SchemeAPIViewMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SchemeSerializer

    def update(self, request, *args, **kwargs):
        request = self.convert_request_data(request)
        return super().update(request, *args, **kwargs)


class SurveyListAPIView(generics.ListAPIView):
    serializer_class = SurveyListSerializer

    def get_queryset(self):
        return Schema.objects.filter(date_to__gte=date.today())


@api_view(['GET'])
def schema_take(request, *, pk):
    participant_id = request.GET.get('participant_id')
    if participant_id:
        participant = Participant.objects.get(pk=participant_id)
    else:
        participant = Participant.objects.create()

    scheme = Schema.objects.get(pk=pk)
    survey = Survey.objects.create(scheme=scheme, participant=participant)
    return redirect('survey-detail', pk=survey.id)


class SurveyDetailAPIView(GetPatchAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def update(self, request, *args, **kwargs):
        answers = []
        for answer_data in request.data.pop('answers'):
            try:
                answer = Answer.objects.select_for_update().get(id=answer_data['id'])
                answer.content = validate_answer(answer, answer_data['answer'])
                answers.append(answer)
            except ObjectDoesNotExist:
                return Response(
                    data={'id': 'No such answer: %s' % answer_data['id']},
                    status=status.HTTP_404_NOT_FOUND
                )

        Answer.objects.bulk_update(answers, fields=['content'])
        return super().update(request, *args, **kwargs)