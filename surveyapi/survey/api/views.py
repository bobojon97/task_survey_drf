from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from survey.models import Schema, Question, Survey
from survey.api.serializers import SchemaSerializer, QuestionSerializer, SurveySerializer


@api_view(['GET'])
def api_versions_list(request, format=None):
    return Response({
        'api2': reverse('api-api2-root', request=request, format=format),
    })