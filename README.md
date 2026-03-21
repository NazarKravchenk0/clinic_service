# 🏥 Clinic Appointment Service

A full-stack clinic appointment management system built with **FastAPI**, **SQLAlchemy**, **SQLite**, and a plain HTML/CSS/JS frontend.

---

## 📁 Project Structure

```
clinic_service/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── database/db.py       # SQLAlchemy engine & session
│   │   ├── models/models.py     # ORM models (Patient, Doctor, Appointment)
│   │   ├── schemas/schemas.py   # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   ├── routers/             # API route handlers
│   │   └── tests/               # Pytest test suite
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── templates/index.html     # Main UI
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── docker/
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

---

## 🚀 Running Locally

### Without Docker

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open: [http://localhost:8000](http://localhost:8000)

API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### With Docker

```bash
docker-compose up --build
```

Open: [http://localhost](http://localhost)

---

## 🔌 API Endpoints

### Patients
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/patients/` | List all patients |
| GET | `/api/patients/{id}` | Get patient by ID |
| POST | `/api/patients/` | Create patient |
| PUT | `/api/patients/{id}` | Update patient |
| DELETE | `/api/patients/{id}` | Delete patient |

### Doctors
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/doctors/` | List all doctors |
| GET | `/api/doctors/{id}` | Get doctor by ID |
| POST | `/api/doctors/` | Create doctor |
| PUT | `/api/doctors/{id}` | Update doctor |
| DELETE | `/api/doctors/{id}` | Delete doctor |

### Appointments
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/appointments/` | List all appointments |
| GET | `/api/appointments/{id}` | Get appointment by ID |
| GET | `/api/appointments/patient/{id}` | Get by patient |
| GET | `/api/appointments/doctor/{id}` | Get by doctor |
| POST | `/api/appointments/` | Create appointment |
| PUT | `/api/appointments/{id}` | Update status/notes |
| DELETE | `/api/appointments/{id}` | Delete appointment |

---

## 🧪 Running Tests

```bash
cd backend
pytest app/tests/ -v
```

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` and configure:

```
DATABASE_URL=sqlite:///./clinic.db
# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/clinic_db
```

---

## 🛠 Tech Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy, Pydantic v2
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: HTML5, CSS3, Vanilla JS
- **Container**: Docker, Docker Compose, Nginx
- **Testing**: Pytest, httpx
