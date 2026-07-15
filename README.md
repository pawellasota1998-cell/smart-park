# Euro Park Parking Management System

A full-stack web application for managing parking space applications
in the Euro Park residential community.

The system allows residents to submit parking applications, supervisors to review them,
and the barrier system to verify vehicle access based on approved applications.

## Tech Stack

### Backend

- Python 3.12+
- FastAPI
- SQLAlchemy 2.x
- Pydantic v2
- Alembic
- Microsoft SQL Server
- JWT authentication
- Refresh token rotation
- Ruff
- Black
- Pytest

### Frontend

- Nuxt 4
- Vue 3
- TypeScript
- Tailwind CSS
- ESLint
- Prettier

### DevOps

- Docker
- Docker Compose

## Features

- User registration and login
- JWT access token authentication
- Refresh token rotation
- User parking applications
- Application status tracking
- Supervisor review panel
- Role-based access control
- Barrier access check
- Request validation
- Error handling
- CORS
- Request ID middleware
- Rate limiting for barrier endpoint
- Swagger/OpenAPI/ReDoc documentation

## Project Structure

```text
.
├── backend/
├── frontend/
├── infra/
├── docker-compose.yml
├── .env.example
└── README.md
````

## Quick Start

### Create the root .env file:

````powershell
Copy-Item .env.example .env
````
### Generate JWT secret:
A secure JWT secret can be generated with:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(64))"
```
Copy the generated value to JWT_SECRET_KEY in the .env file.

## Update secrets in .env:
````
MSSQL_SA_PASSWORD=...

DB_PASSWORD=...

JWT_SECRET_KEY=...
````
Do not commit the .env file to the repository.


### Start SQL Server:

````powershell
docker compose up -d
````

### Run backend:

````powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m alembic upgrade head
python -m uvicorn app.main:app --reload
````

### Run frontend:

````powershell
cd frontend
npm install
npm run dev
````
#### Backend:
````http
http://127.0.0.1:8000
````
#### Frontend::
````http
http://localhost:3000
````

#### API docs:
````http
http://127.0.0.1:8000/docs
````

### Demo Accounts

#### Create demo users

````powershell
cd backend
python -m scripts.seed_demo_users
````
#### User:
````text
email: user@example.com
password: Password123!
````

#### Supervisor:
````text
email: supervisor@example.com
password: Password123!
````

### Demo Flow

1. Log in as user@example.com.
2. Create a parking application.
3. Log out.
4. Log in as supervisor@example.com.
5. Approve the application.
6. Open /barrier.
7. Check access for the approved registration number.

### Quality Checks

#### Backend:
````powershell
cd backend
python -m pytest -v
python -m ruff check .
python -m black --check .
python -m alembic check
````

#### Frontend:
````powershell
cd frontend
npm run lint
npm run build
````


### Backend documentation:
````
backend/README.md
````

### Frontend documentation:
````
frontend/README.md
````