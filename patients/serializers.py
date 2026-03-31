from rest_framework import serializers
from patients.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "first_name", "last_name", "email", "phone", "date_of_birth"]


class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["first_name", "last_name", "phone", "date_of_birth"]
        extra_kwargs = {f: {"required": False} for f in fields}
