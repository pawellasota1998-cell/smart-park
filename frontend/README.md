# Euro Park Frontend

Nuxt frontend for the Euro Park Parking Management System.

## Features

- User registration
- User login
- JWT token storage in cookies
- Auth middleware
- Guest middleware
- Supervisor middleware
- User dashboard
- User parking applications
- Supervisor application review panel
- Barrier access screen
- API error handling

### Environment Variables

Create `.env` from `.env.example`:

```powershell
Copy-Item .env.example .env
```

### Default API URL:
````http
NUXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
````

### Install Dependencies
```powershell
npm install
```
### Run Development Server
```powershell
npm run dev
```

Frontend will be available at:
````http
http://localhost:3000
````

## Main Routes

````text
/                           Home page
/health                     Backend health check
/login                      User login
/register                   User registration
/dashboard                  User dashboard
/supervisor/applications    Supervisor panel
/barrier                    Barrier access check
````

## User Applications
The user dashboard allows authenticated users to:

- create parking applications,
- list their own applications,
- edit applications in PENDING or NEEDS_CHANGES status,
- see supervisor comments,
- see application statuses.

## Supervisor Panel
The supervisor panel allows users with SUPERVISOR or ADMIN role to:

- list parking applications,
- filter by status,
- filter by registration number,
- sort results,
- use pagination,
- approve applications,
- reject applications,
- request changes with a comment.

## Barrier Screen

The frontend includes a public barrier access screen:

````http
/barrier
````
It allows checking whether a vehicle registration number has access to the parking area.

Access is granted only when there is an approved parking application for the provided registration number.

### Quality Checks
```powershell
npm run lint
npm run format:check
npm run build
```
To format files:
```powershell
npm run format
```