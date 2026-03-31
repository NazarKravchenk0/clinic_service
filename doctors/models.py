from django.db import models


class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True, db_index=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "doctors"

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"
