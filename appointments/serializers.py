from rest_framework import serializers
from appointments.models import Appointment, AppointmentStatus
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    doctor_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id", "patient_id", "doctor_id",
            "patient", "doctor",
            "appointment_date", "status", "notes",
        ]


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["patient_id", "doctor_id", "appointment_date", "notes"]


class AppointmentUpdateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=AppointmentStatus.choices, required=False)

    class Meta:
        model = Appointment
        fields = ["appointment_date", "status", "notes"]
        extra_kwargs = {f: {"required": False} for f in fields}
