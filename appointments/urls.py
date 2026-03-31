from django.urls import path
from appointments.views import (
    AppointmentListCreateView,
    AppointmentDetailView,
    AppointmentByPatientView,
    AppointmentByDoctorView,
)

urlpatterns = [
    path("", AppointmentListCreateView.as_view()),
    path("<int:pk>/", AppointmentDetailView.as_view()),
    path("patient/<int:patient_id>/", AppointmentByPatientView.as_view()),
    path("doctor/<int:doctor_id>/", AppointmentByDoctorView.as_view()),
]
