from django.test import TestCase

# Create your tests here.
import pytest  
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restispecApp.settings')
django.setup()
from .models import Acquisition,Patient
## This is a unit test for Acquisition model creation using mock database which asserts the created data 
# is really stored in the mock database.
@pytest.mark.django_db  
def test_acquisition_create():
# Create Patient data  
    patient = Patient.objects.create(  
                first_name="Erden",  
                last_name="Oktay", 
                dob="1997-02-23",  
                sex="Male",  
               )  
    assert patient!=None
    acquisition = Acquisition.objects.create(  
                eye="right",  
                site_name="XYZ", 
                patient=patient,
                date_taken="1997-08-23",  
                operator_name="Maine",  
               )  
# Assert the Created data saved as we expected
    assert acquisition!=None
    assert acquisition.eye=="right"  
    assert acquisition.site_name=="XYZ"  
    assert acquisition.date_taken=="1997-08-23"  
    assert acquisition.operator_name=="Maine"
    assert acquisition.patient_id==patient.id