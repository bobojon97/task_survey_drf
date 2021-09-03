from django.urls import path
from rest_framework.schemas import get_schema_view
from survey.apis.views import *

urlpatterns = [
    path('', api_api2_root, name='api2-root'),
    path('schemas/', SchemeListAPIView.as_view(), name='scheme-list'),
    path('schemas/<uuid:pk>', SchemeDetailAPIView.as_view(), name='scheme-detail'),
    path('schemas/<uuid:pk>/take', schema_take, name='scheme-take'),
    path('surveys/', SurveyListAPIView.as_view(), name='survey-list'),
    path('surveys/<uuid:pk>', SurveyDetailAPIView.as_view(), name='survey-detail'),
    path('participants/', ParticipantListAPIView.as_view(), name='participant-list'),
    # path('participants/<int:pk>', ParticipantDetailAPIView.as_view(), name='participant-detail')
]