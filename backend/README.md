# Euro Park API

Backend REST API for managing parking applications in the Euro Park residential community.

## Tech stack

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
- Docker Compose


## Features

- User registration
- Login with JWT access token
- Refresh token rotation
- Logout through refresh token revocation
- Current user endpoint
- User parking applications
- Supervisor application review
- Role-based access control
- Barrier access check
- Input validation
- HTTP error handling
- Request ID middleware
- CORS
- Basic rate limiting for barrier endpoint
- Customized Swagger UI, OpenAPI schema, and ReDoc documentation

## Requirements

- Python 3.12+
- Docker Desktop
- Microsoft ODBC Driver 18 for SQL Server

Docker Desktop must be running before starting the database containers.

## Environment variables

From the project root, create the .env file from .env.example:

```powershell
Copy-Item .env.example .env
```

## Update secrets in .env:
````
MSSQL_SA_PASSWORD=...

DB_PASSWORD=...

JWT_SECRET_KEY=...
````
Do not commit the .env file to the repository.


## Generate JWT secret:
A secure JWT secret can be generated with:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(64))"
```
Copy the generated value to JWT_SECRET_KEY in the .env file.

## Run SQL Server
Run the following commands from the project root:
```powershell
docker compose up -d
docker compose ps
```
The SQL Server container should have the healthy status before running migrations.

To stop the containers:

```powershell
docker compose down
```

## Install backend dependencies
Go to the backend directory:
```powershell
cd backend
```

Create and activate a virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```
Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run database migrations
Run the migrations from the backend directory with the virtual environment activated:
```powershell
python -m alembic upgrade head
python -m alembic current
```

## Run API
Start the development server:
```powershell
python -m uvicorn app.main:app --reload
```
The API will be available at:

    http://127.0.0.1:8000

## API documentation:
Swagger UI:
````
http://127.0.0.1:8000/docs
````
ReDoc:
````
http://127.0.0.1:8000/redoc
````
OpenAPI schema:
````
http://127.0.0.1:8000/openapi.json
````

## Quality checks
Run the following commands from the backend directory

```powershell
python -m pytest -v
python -m ruff check .
python -m black --check .
python -m alembic check
```
To automatically format the source code with Black:
```powershell
python -m black .
```

To apply automatically fixable Ruff changes:

```powershell
python -m ruff check . --fix
```

## Main endpoints

### Authentication
````
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
GET  /api/v1/auth/me
````

### User applications
````
POST  /api/v1/applications
GET   /api/v1/applications/me
GET   /api/v1/applications/{application_id}
PATCH /api/v1/applications/{application_id}
````
### Supervisor
````
GET   /api/v1/supervisor/applications
PATCH /api/v1/supervisor/applications/{application_id}/approve
PATCH /api/v1/supervisor/applications/{application_id}/reject
PATCH /api/v1/supervisor/applications/{application_id}/request-changes
````
### Barrier
````
POST /api/v1/barrier/check-access
````
### Health
````
GET /api/v1/health
GET /api/v1/health/ready
````

## Demo flow

1. Register a regular user.
2. Log in as the registered user.
3. Create a parking application.
4. Register another user who will act as the supervisor.
5. Promote the second user to supervisor manually in SQL Server:
```sql
UPDATE dbo.users
SET role = N'SUPERVISOR'
WHERE email = N'supervisor@example.com';
```
6. Log in again as the supervisor to obtain a new access token.
7. Approve, reject, or request changes to the parking application.
8. Check vehicle access using: POST /api/v1/barrier/check-access

