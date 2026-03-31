from django.db import models


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True, db_index=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "patients"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
