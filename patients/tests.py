from django.test import TestCase

# Create your tests here.
import pytest  
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retispecApp.settings')
django.setup()
from .models import Patient  
# This is unit testing for creating Patient record using mock database.
@pytest.mark.django_db  
def test_patient_create():
# Create Patient data  
    patient = Patient.objects.create(  
                first_name="Muhammed",  
                last_name="Ali", 
                dob="1997-02-23",  
                sex="Male",  
               )  
# Assert the Created data saved as expected.
    assert patient.first_name=="Muhammed"  
    assert patient.last_name=="Ali"  
    assert patient.dob=="1997-02-23"  
    assert patient.sex=="Male"