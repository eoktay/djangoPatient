import datetime
import os
from django.db import models

from patients.models import Patient
# This function returns filename to store image data using current date time.
def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

# Create your models here.
class Acquisition(models.Model):
    class Meta:
        ordering = ['id']
        db_table = "acquisitions"
    eye = models.CharField(max_length=50,choices=[('right','RIGHT'),('left','LEFT'),])
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,related_name='paient_acquisition')
    site_name = models.CharField(max_length=50)
    date_taken=  models.DateField(auto_now=False,auto_now_add=False)
    operator_name=  models.CharField(max_length=10)
    image_data=models.ImageField(upload_to=filepath, null=True, blank=True)

