from django.urls import path
from django.urls.conf import include
from survey.api.views import ExampleView

urlpatterns = [
    path("", ExampleView, name="api-version-list"),
    path("api2/", include("api.api2.urls"), name="api2")
]