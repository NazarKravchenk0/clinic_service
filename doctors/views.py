from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from doctors.models import Doctor
from doctors.serializers import DoctorSerializer, DoctorUpdateSerializer


class DoctorListCreateView(APIView):
    def get(self, request):
        doctors = Doctor.objects.all()
        return Response(DoctorSerializer(doctors, many=True).data)

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        if Doctor.objects.filter(email=email).exists():
            return Response({"detail": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)
        doctor = serializer.save()
        return Response(DoctorSerializer(doctor).data, status=status.HTTP_201_CREATED)


class DoctorDetailView(APIView):
    def get(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        return Response(DoctorSerializer(doctor).data)

    def put(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        serializer = DoctorUpdateSerializer(doctor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(DoctorSerializer(doctor).data)

    def delete(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        doctor.delete()
        return Response({"detail": "Doctor deleted"})
