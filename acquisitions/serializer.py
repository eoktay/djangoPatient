from .models import Acquisition
from rest_framework import serializers

# AcquisitionSerializer used to serialize Acquisition model created before.
class AcquisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acquisition
        fields = ["id","eye","patient","site_name","date_taken","operator_name","image_data"]