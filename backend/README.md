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
```` http
http://127.0.0.1:8000/docs
````
ReDoc:
```` http
http://127.0.0.1:8000/redoc
````
OpenAPI schema:
```` http
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
```` http
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
GET  /api/v1/auth/me
````

### User applications
```` http
POST  /api/v1/applications
GET   /api/v1/applications/me
GET   /api/v1/applications/{application_id}
PATCH /api/v1/applications/{application_id}
````
### Supervisor
```` http
GET   /api/v1/supervisor/applications
PATCH /api/v1/supervisor/applications/{application_id}/approve
PATCH /api/v1/supervisor/applications/{application_id}/reject
PATCH /api/v1/supervisor/applications/{application_id}/request-changes
```` 
### Barrier
```` http
POST /api/v1/barrier/check-access
````
### Health
```` http
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

## Example requests and responses

The examples below use placeholder IDs, timestamps, and JWT tokens. Actual values will be different.

Protected endpoints require an access token in the following header:

```http
Authorization: Bearer <access_token>
```

### Register a user

#### Request

```http
POST /api/v1/auth/register
Content-Type: application/json
```

```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!",
  "first_name": "John",
  "last_name": "Smith"
}
```

#### Example response

```http
HTTP/1.1 201 Created
Content-Type: application/json
```

```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Smith",
  "role": "USER",
  "is_active": true,
  "created_at": "2026-07-14T10:30:00"
}
```

### Log in

The login endpoint uses the OAuth2 password form. The request body must be sent as `application/x-www-form-urlencoded`, not JSON.

The user's email address is passed in the `username` field.

#### Request

```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded
```

```text
username=user@example.com&password=StrongPassword123!
```

#### Example response

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "access_token": "<access_token>",
  "refresh_token": "<refresh_token>",
  "token_type": "bearer",
  "expires_in": 900
}
```

### Get the current user

#### Request

```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

#### Example response

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Smith",
  "role": "USER",
  "is_active": true,
  "created_at": "2026-07-14T10:30:00"
}
```

### Refresh an access token

Refresh tokens are rotated. After a successful refresh, the previous refresh token is revoked and must not be used again.

#### Request

```http
POST /api/v1/auth/refresh
Content-Type: application/json
```

```json
{
  "refresh_token": "<refresh_token>"
}
```

#### Example response

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "access_token": "<new_access_token>",
  "refresh_token": "<new_refresh_token>",
  "token_type": "bearer",
  "expires_in": 900
}
}
```

### Log out

Logging out revokes the provided refresh token.

#### Request

```http
POST /api/v1/auth/logout
Content-Type: application/json
```

```json
{
  "refresh_token": "<refresh_token>"
}
```

#### Example response

```http
HTTP/1.1 204 No Content
```

### Create a parking application

#### Request

```http
POST /api/v1/applications
Authorization: Bearer <access_token>
Content-Type: application/json
```

```json
{
  "registration_number": "WX12345",
  "preferred_floor": 2
}
```

The registration number is normalized to uppercase and must contain between 4 and 10 letters or digits.

#### Example response

```http
HTTP/1.1 201 Created
Content-Type: application/json
```

```json
{
  "id": 2002,
  "user_id": 1002,
  "registration_number": "WWE5677",
  "preferred_floor": -5,
  "status": "PENDING",
  "supervisor_comment": null,
  "reviewed_by_user_id": null,
  "reviewed_at": null,
  "created_at": "2026-07-14T09:53:42.976324",
  "updated_at": "2026-07-14T09:53:42.976324"
}
```

### List the current user's applications

#### Request

```http
GET /api/v1/applications/me
Authorization: Bearer <access_token>
```

#### Example response

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
[  
  {
    "id": 2002,
    "user_id": 1002,
    "registration_number": "WWE5677",
    "preferred_floor": -5,
    "status": "PENDING",
    "supervisor_comment": null,
    "reviewed_by_user_id": null,
    "reviewed_at": null,
    "created_at": "2026-07-14T09:53:42.976324",
    "updated_at": "2026-07-14T09:53:42.976324"
  }
]
```

### List applications as a supervisor

This endpoint requires a user with the `SUPERVISOR` or `ADMIN` role.

Available query parameters include:

* `status`
* `registration_number`
* `page`
* `page_size`
* `sort_by`
* `sort_order`

#### Request

```http
GET /api/v1/supervisor/applications?status=PENDING&page=1&page_size=20&sort_by=created_at&sort_order=desc
Authorization: Bearer <supervisor_access_token>
```

#### Example response

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "items": [
    {
      "id": 1,
      "user_id": 1,
      "registration_number": "WX12345",
      "preferred_floor": 2,
      "status": "PENDING",
      "supervisor_comment": null,
      "reviewed_by_user_id": null,
      "reviewed_at": null,
      "created_at": "2026-07-14T10:45:00"
    }
  ],
  "page": 1,
  "page_size": 20,
  "total_items": 1,
  "total_pages": 1
}
```

### Approve a parking application

#### Request

```http
PATCH /api/v1/supervisor/applications/1/approve
Authorization: Bearer <supervisor_access_token>
```

#### Example response

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "id": 1,
  "user_id": 1,
  "registration_number": "WX12345",
  "preferred_floor": 2,
  "status": "APPROVED",
  "supervisor_comment": null,
  "reviewed_by_user_id": 2,
  "reviewed_at": "2026-07-14T11:00:00",
  "created_at": "2026-07-14T10:45:00"
}
```

### Reject a parking application

#### Request

```http
PATCH /api/v1/supervisor/applications/1/reject
Authorization: Bearer <supervisor_access_token>
Content-Type: application/json
```

```json
{
  "comment": "No parking spaces are currently available."
}
```

#### Example response

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "id": 1,
  "user_id": 1,
  "registration_number": "WX12345",
  "preferred_floor": 2,
  "status": "REJECTED",
  "supervisor_comment": "No parking spaces are currently available.",
  "reviewed_by_user_id": 2,
  "reviewed_at": "2026-07-14T11:05:00",
  "created_at": "2026-07-14T10:45:00"
}
```

### Check barrier access

The barrier endpoint verifies whether the registration number belongs to an approved parking application.

#### Request

```http
POST /api/v1/barrier/check-access
Content-Type: application/json
```

```json
{
  "registration_number": "WX12345"
}
```

#### Example response for an approved vehicle

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "registration_number": "WX12345",
  "access_granted": true
}
```

#### Example response for a vehicle without an approved application

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "registration_number": "WA98765",
  "access_granted": false
}
```

### Example authentication error

A protected endpoint called without a valid access token returns:

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json
```

```json
{
  "detail": {
    "code": "INVALID_ACCESS_TOKEN",
    "message": "Authentication credentials could not be validated.",
    "request_id": "0bc0a3a8-25c9-4d13-baf0-c46f9eb2cc75"
  }
}
```

### Example validation error

An invalid registration number may return:

```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/json
```

```json
{
  "detail": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "errors": [
      {
        "type": "value_error",
        "location": [
          "body",
          "registration_number"
        ],
        "message": "Value error, invalid registration number format"
      }
    ],
    "request_id": "2fc5e899-d3cb-4ed5-a037-8cd29cac67aa"
  }
}
```
