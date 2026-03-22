import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def patient_and_doctor(client):
    p = client.post("/api/patients/", {
        "first_name": "Test",
        "last_name": "Patient",
        "email": "appt.patient@example.com",
    }, format="json").json()
    d = client.post("/api/doctors/", {
        "first_name": "Test",
        "last_name": "Doctor",
        "specialization": "GP",
        "email": "appt.doctor@clinic.com",
    }, format="json").json()
    return p["id"], d["id"]


def test_create_appointment(client, patient_and_doctor):
    pid, did = patient_and_doctor
    response = client.post("/api/appointments/", {
        "patient_id": pid,
        "doctor_id": did,
        "appointment_date": "2025-06-15T10:00:00",
        "notes": "Routine checkup",
    }, format="json")
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "scheduled"
    assert data["patient"]["id"] == pid
    assert data["doctor"]["id"] == did


def test_get_appointments(client):
    response = client.get("/api/appointments/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_appointment_status(client, patient_and_doctor):
    pid, did = patient_and_doctor
    create = client.post("/api/appointments/", {
        "patient_id": pid,
        "doctor_id": did,
        "appointment_date": "2025-07-10T14:00:00",
    }, format="json")
    aid = create.json()["id"]
    response = client.put(f"/api/appointments/{aid}/", {"status": "completed"}, format="json")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_delete_appointment(client, patient_and_doctor):
    pid, did = patient_and_doctor
    create = client.post("/api/appointments/", {
        "patient_id": pid,
        "doctor_id": did,
        "appointment_date": "2025-08-01T09:00:00",
    }, format="json")
    aid = create.json()["id"]
    response = client.delete(f"/api/appointments/{aid}/")
    assert response.status_code == 200
    gone = client.get(f"/api/appointments/{aid}/")
    assert gone.status_code == 404


def test_get_appointments_by_patient(client, patient_and_doctor):
    pid, did = patient_and_doctor
    response = client.get(f"/api/appointments/patient/{pid}/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_appointments_by_doctor(client, patient_and_doctor):
    pid, did = patient_and_doctor
    response = client.get(f"/api/appointments/doctor/{did}/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
