from django.urls import path
from .views import WorksAPIView

app_name = "core"

urlpatterns = [
    path("", WorksAPIView.as_view(), name="works-single-view"),
]
