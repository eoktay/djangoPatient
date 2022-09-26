from .models import Patient
from rest_framework import serializers

#PatientSerializer is used serialize a Patient model to validate and format data.
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id","first_name","last_name","dob","sex"]