from django.urls import path
from django.urls.conf import include
from survey.api.views import api_versions_list

urlpatterns = [
    path("", api_versions_list, name="api-version-list"),
    path("apis/", include("survey.apis.urls"), name="apis")
]