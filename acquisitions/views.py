import datetime
from email.mime import base
from http import HTTPStatus
from http.client import HTTPResponse
import os
import traceback
from acquisitions.models import Acquisition
from patients.models import Patient
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework import status, viewsets, views
from rest_framework.permissions import  AllowAny
from django.http.response import HttpResponse
import pathlib


from retispecApp import settings



from django.db import transaction
from wsgiref.util import FileWrapper

import mimetypes
from utils.utils import MODEL_DELETE_FAILED, error_response, success_response,MODEL_PARAM_MISSED,MODEL_RECORD_NOT_FOUND,MODEL_ALREADY_EXIST
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .serializer import AcquisitionSerializer
# AcquisitionViewSet controls a request related to Patient Acquisition model.
class AcquisitionViewSet(viewsets.ModelViewSet):
    serializer_class = AcquisitionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["id"]
    search_fields = ["eye","site_name","operator_name"]
    filter_fields = ["eye","operator_name","date_taken","site_name"]
    # get_queryset returns a query set dependent on the urls pattern.
    # If request comes with /acquisitions?patient_id=1 the data returned is only Acquisition model record
    # whose patient id is 1.
    # Iff request comes without query param it will return all data record in the Acquisitions model.
    def get_queryset(self):
        queryset = Acquisition.objects.all()
        patient_id=self.request.query_params.get('patient_id',None)
        if patient_id is not None:
            #return a patient with first name and last name lookup
            patient=Acquisition.objects.filter(patient__id=int(patient_id))
            return patient
        return queryset
    # This function retrieves a single data record for acquisitions whose id matches with url param given.
    def retrieve(self, request, pk=None):
        if not pk.isdigit():
            res = error_response(request, MODEL_PARAM_MISSED, "Acquisition")
            res['message']='Invalid request parameter found.'
            return Response(res,status=int(res['status_code']), content_type="application/json")
        try:
            queryset = Acquisition.objects.get(pk=pk)
        except:
            res = error_response(request, MODEL_RECORD_NOT_FOUND, "Acquisition")
            res['message']='Acquisition not found with id '+pk+"."
            return Response(res,status=int(res['status_code']), content_type="application/json")
        serializer=AcquisitionSerializer(queryset)
        return Response(serializer.data)

    # This function creates new instance of acquisitions if not there before.
    def create(self, request, *args, **kwargs):
        print("creating ...")      
        data = request.POST
        count = Acquisition.objects.filter(eye__iexact=data["eye"],site_name__iexact=data["site_name"],date_taken__iexact=data["date_taken"]).count()
        print("Count ", count)
        if count > 0:
            res = error_response(request, MODEL_ALREADY_EXIST, "Acquisition")
            return Response(res,status=int(res['status_code']), content_type="application/json")
        else:
            pass
        patient_obj=None
        try:
            patient_obj = Patient.objects.get(pk=data['patient'])
        except:
            res = error_response(request, MODEL_RECORD_NOT_FOUND, "Patinet")
            res['message']='Patinet not found with id '+data['patient']+"."
            return Response(res,status=int(res['status_code']), content_type="application/json")
        if len(request.FILES) == 0:
            res = error_response(request, MODEL_PARAM_MISSED, "Acquisition")
            res['message']='Image file is a required field.'
            return Response(res,status=int(res['status_code']), content_type="application/json")
        
        acquisition_obj = Acquisition.objects.create(
            eye=data["eye"],
            patient=patient_obj,
            site_name=data["site_name"],
            date_taken=data["date_taken"],
            operator_name=data["operator_name"],
            image_data=request.FILES['image'],
            )
        serializer = AcquisitionSerializer(acquisition_obj)
        data = (serializer.data)
        return Response((data))
    # This function removes or deletes a single instance of Acquisitions whose id number matches 
    # the number provided in the url param.
    def destroy(self, request, *args, **kwargs):
        print("deleting ...")
        instance = Acquisition.objects.filter(id=kwargs["pk"])
        if len(instance) != 1:
            res = error_response(self.request, MODEL_DELETE_FAILED, "Acquisition")
            res['message']='Unable to remove patient acquisition.'
            return Response(res, status=int(res['status_code']),content_type="application/json")
        instance.delete()
        return Response({"code":204, "result": "Acquisition instance was successfuly deleted!"})
# DownloadImageFile: this viewset is used to download a single image identified by the acquisition id number.
class DownloadImageFile(views.APIView):
    permission_classes = [AllowAny]
    # Download an image file from server using Acquisition id number.
    def get(self, request, *args, **kwargs):
        try:
            id = request.query_params['id']
            acquisition = Acquisition.objects.get(id=id)
            if acquisition is None:
                res = error_response(self.request, MODEL_RECORD_NOT_FOUND, "Acquisition")
                res['message']='Resource not found.'
                return Response(res, status=int(res['status_code']),content_type="application/json")
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path=os.path.join(BASE_DIR,acquisition.image_data.path)
            image = open(path, 'rb')
            mime_type, _ = mimetypes.guess_type(path)
            response = HttpResponse(FileWrapper(image),content_type=mime_type)
            extension = pathlib.Path(path).suffix
            time_now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            filename = "%s_image_file%s" % (time_now,extension)
            response['Content-Disposition'] = 'attachment; filename={}'.format((filename))
            return response
        except Exception as e:
            traceback.print_exc()
            return Response({'detail': str(e)}, status=HTTP_404_NOT_FOUND)


