import pytest

pytestmark = pytest.mark.django_db


def test_create_patient(client):
    response = client.post("/api/patients/", {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15",
    }, format="json")
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "john.doe@example.com"
    assert data["first_name"] == "John"
    assert "id" in data


def test_get_patients(client):
    response = client.get("/api/patients/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_patient_by_id(client):
    create = client.post("/api/patients/", {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
    }, format="json")
    pid = create.json()["id"]
    response = client.get(f"/api/patients/{pid}/")
    assert response.status_code == 200
    assert response.json()["id"] == pid


def test_update_patient(client):
    create = client.post("/api/patients/", {
        "first_name": "Bob",
        "last_name": "Brown",
        "email": "bob.brown@example.com",
    }, format="json")
    pid = create.json()["id"]
    response = client.put(f"/api/patients/{pid}/", {"phone": "+9998887776"}, format="json")
    assert response.status_code == 200
    assert response.json()["phone"] == "+9998887776"


def test_delete_patient(client):
    create = client.post("/api/patients/", {
        "first_name": "Del",
        "last_name": "User",
        "email": "del.user@example.com",
    }, format="json")
    pid = create.json()["id"]
    response = client.delete(f"/api/patients/{pid}/")
    assert response.status_code == 200
    gone = client.get(f"/api/patients/{pid}/")
    assert gone.status_code == 404


def test_duplicate_email(client):
    client.post("/api/patients/", {
        "first_name": "Dup",
        "last_name": "Test",
        "email": "dup@example.com",
    }, format="json")
    response = client.post("/api/patients/", {
        "first_name": "Dup2",
        "last_name": "Test2",
        "email": "dup@example.com",
    }, format="json")
    assert response.status_code == 400
