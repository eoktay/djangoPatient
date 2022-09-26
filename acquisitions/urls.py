from django.urls import path
from rest_framework import routers

from .views import AcquisitionViewSet, DownloadImageFile
# This is a simple router to register url for a given viewset.
# AcquisitionViewSet and DownloadImageFile viewsets are registered through here.
router = routers.SimpleRouter(trailing_slash=False)
router.register("acquisition", AcquisitionViewSet, basename="acquisition")
urlpatterns=[
        path('image/download',(DownloadImageFile.as_view()))
    ]+router.urls