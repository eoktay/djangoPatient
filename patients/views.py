from http import HTTPStatus
from acquisitions.models import Acquisition
from patients.models import Patient
from django.db import transaction
from utils.utils import MODEL_DELETE_FAILED, error_response, success_response,MODEL_PARAM_MISSED,MODEL_RECORD_NOT_FOUND,MODEL_ALREADY_EXIST
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from rest_framework.permissions import  AllowAny


from .serializer import PatientSerializer
# This viewset controls all request coming through /patients request path including url param and query param.
class PatientViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["id"]
    search_fields = ["first_name","last_name"]
    filter_fields = ["first_name","last_name","dob","sex"]
    # get_queryset returns a queryset for a user requet.
    # If a user request comes with query params of first name and last name, it filters the Patient model by using first name 
    # and last name. Then, it returns a result query set for request response e.g /patients?first_name=ABC&last_name=XYZ
    # If a user request comes without any query param like /patients, it will return 
    # all Patient records available in the database as queryset.
    def get_queryset(self):
        queryset = Patient.objects.all()
        first_name=self.request.query_params.get('first_name',None)
        last_name=self.request.query_params.get('last_name',None)
        if first_name is not None and last_name is not None:
            #return a patient with first name and last name lookup
            patient=Patient.objects.filter(first_name__iexact=first_name,last_name__iexact=last_name)
            return patient
        return queryset
    # This function returns a single instance of Patient identified by an id coming from the url 
    # param like /patients/1
    def retrieve(self, request, pk=None):
        
        if not pk.isdigit():
            res = error_response(request, MODEL_PARAM_MISSED, "Patient")
            res['message']='Invalid request parameter found.'
            return Response(res,status=int(res['status_code']), content_type="application/json")
        try:
            queryset = Patient.objects.get(pk=pk)
        except:
            res = error_response(request, MODEL_RECORD_NOT_FOUND, "Patient")
            res['message']='Patient not found with id '+pk+"."
            return Response(res,status=int(res['status_code']), content_type="application/json")
        serializer=PatientSerializer(queryset)
        return Response(serializer.data,status=HTTPStatus.OK,content_type="application/json")

    # This function creates new instance of Patient models if not registered before.
    def create(self, request, *args, **kwargs):
        print("creating ...")
        data = request.data
        count = Patient.objects.filter(first_name__iexact=data["first_name"],last_name__iexact=data["last_name"]).count()
        print("Count ", count)
        if count > 0:
            res = error_response(request, MODEL_ALREADY_EXIST, "Patient")
            res["message"]="Patient already registered."
            return Response(res,status=int(res['status_code']), content_type="application/json")
        else:
            pass
        patient_obj = Patient.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            dob=data["dob"],
            sex=data["sex"],
            )
        serializer = PatientSerializer(patient_obj)
        data = (serializer.data)
        return Response((data))
    # This function removes or deletes a single instance of Patient whose id number matches 
    # with the number provided in the url param like /patients/2
    def destroy(self, request, *args, **kwargs):
        print("deleting ...")
        instance = Patient.objects.filter(id=kwargs["pk"])
        if len(instance) != 1:
            res = error_response(self.request, MODEL_DELETE_FAILED, "Patient")
            res['message']='Unable to remove patient.'
            return Response(res, status=int(res['status_code']),content_type="application/json")
        instance.delete()
        return Response({"code":204, "result": "Acquisition instance was successfuly deleted!"})



