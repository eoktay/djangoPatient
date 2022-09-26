from xml.parsers.expat import model
from django.db import models

# Create your models here.
# Patient model is used to record patient information like first name, last name, dob and gender.
class Patient(models.Model):
    class Meta:
        ordering = ['id']
        db_table = "patients"
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob=  models.DateField()
    sex=  models.CharField(max_length=10)