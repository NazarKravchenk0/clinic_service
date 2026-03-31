from rest_framework import serializers
from doctors.models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["id", "first_name", "last_name", "specialization", "email", "phone"]


class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["first_name", "last_name", "specialization", "phone"]
        extra_kwargs = {f: {"required": False} for f in fields}
