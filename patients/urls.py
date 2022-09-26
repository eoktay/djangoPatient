from rest_framework import routers

from .views import PatientViewSet
# Matches the viewset with its url via simple router.
router = routers.SimpleRouter(trailing_slash=False)
router.register("patients", PatientViewSet, basename="patients")
urlpatterns = router.urls