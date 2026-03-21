def test_create_doctor(client):
    response = client.post("/api/doctors/", json={
        "first_name": "Alice",
        "last_name": "Walker",
        "specialization": "Cardiologist",
        "email": "alice.walker@clinic.com",
        "phone": "+1112223333"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["specialization"] == "Cardiologist"
    assert "id" in data


def test_get_doctors(client):
    response = client.get("/api/doctors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_doctor_by_id(client):
    create = client.post("/api/doctors/", json={
        "first_name": "Mark",
        "last_name": "Evans",
        "specialization": "Neurologist",
        "email": "mark.evans@clinic.com"
    })
    did = create.json()["id"]
    response = client.get(f"/api/doctors/{did}")
    assert response.status_code == 200
    assert response.json()["id"] == did


def test_update_doctor(client):
    create = client.post("/api/doctors/", json={
        "first_name": "Tom",
        "last_name": "Hill",
        "specialization": "Surgeon",
        "email": "tom.hill@clinic.com"
    })
    did = create.json()["id"]
    response = client.put(f"/api/doctors/{did}", json={"specialization": "Orthopedic Surgeon"})
    assert response.status_code == 200
    assert response.json()["specialization"] == "Orthopedic Surgeon"


def test_delete_doctor(client):
    create = client.post("/api/doctors/", json={
        "first_name": "Del",
        "last_name": "Doc",
        "specialization": "GP",
        "email": "del.doc@clinic.com"
    })
    did = create.json()["id"]
    response = client.delete(f"/api/doctors/{did}")
    assert response.status_code == 200
    gone = client.get(f"/api/doctors/{did}")
    assert gone.status_code == 404


def test_doctor_not_found(client):
    response = client.get("/api/doctors/99999")
    assert response.status_code == 404
