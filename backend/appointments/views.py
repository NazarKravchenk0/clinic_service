from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentCreateSerializer, AppointmentUpdateSerializer


def _full(appt):
    return AppointmentSerializer(
        Appointment.objects.select_related("patient", "doctor").get(pk=appt.pk)
    ).data


class AppointmentListCreateView(APIView):
    def get(self, request):
        appts = Appointment.objects.select_related("patient", "doctor").all()
        return Response(AppointmentSerializer(appts, many=True).data)

    def post(self, request):
        serializer = AppointmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appt = serializer.save()
        return Response(_full(appt), status=status.HTTP_201_CREATED)


class AppointmentDetailView(APIView):
    def get(self, request, pk):
        appt = get_object_or_404(Appointment.objects.select_related("patient", "doctor"), pk=pk)
        return Response(AppointmentSerializer(appt).data)

    def put(self, request, pk):
        appt = get_object_or_404(Appointment, pk=pk)
        serializer = AppointmentUpdateSerializer(appt, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_full(appt))

    def delete(self, request, pk):
        appt = get_object_or_404(Appointment, pk=pk)
        appt.delete()
        return Response({"detail": "Appointment deleted"})


class AppointmentByPatientView(APIView):
    def get(self, request, patient_id):
        appts = Appointment.objects.select_related("patient", "doctor").filter(patient_id=patient_id)
        return Response(AppointmentSerializer(appts, many=True).data)


class AppointmentByDoctorView(APIView):
    def get(self, request, doctor_id):
        appts = Appointment.objects.select_related("patient", "doctor").filter(doctor_id=doctor_id)
        return Response(AppointmentSerializer(appts, many=True).data)
