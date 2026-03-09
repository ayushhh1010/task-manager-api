# Task Manager API ✅

A production-ready RESTful API built with **FastAPI**, **MongoDB**, **Redis**, and **Celery**. Features JWT authentication, background email notifications, and a clean modular architecture.

---

## Tech Stack 

| Layer | Technology |
|---|---|
| Framework | FastAPI  | 
| Database | MongoDB Atlas + Beanie ODM |
| Auth | JWT (Access + Refresh Tokens) |
| Background Jobs | Celery + Redis |
| Email | Resend API |
| Validation | Pydantic v2 |
| Server | Uvicorn |

---

## Features

- **JWT Authentication** — Register, login, access + refresh token flow
- **Task CRUD** — Create, read, update, delete tasks with full validation
- **Protected Routes** — All task endpoints require a valid JWT token
- **Background Jobs** — Email notifications sent asynchronously via Celery
- **Real Emails** — Transactional emails delivered via Resend API
- **Pagination & Filtering** — Filter tasks by status/priority, paginate results
- **Global Error Handling** — Clean JSON error responses across the entire app
- **Auto Docs** — Swagger UI available at `/docs`

---

## Project Structure

```
task-manager-api/
├── app/
│   ├── main.py               # App entry point, lifespan, global error handler
│   ├── celery_app.py         # Celery instance and configuration
│   ├── tasks.py              # Background job definitions
│   ├── routers/
│   │   ├── auth.py           # Register, login routes
│   │   └── tasks.py          # Task CRUD routes
│   ├── models/
│   │   ├── user.py           # User MongoDB document model
│   │   └── task.py           # Task MongoDB document model
│   ├── schemas/
│   │   ├── user.py           # User request/response schemas
│   │   └── task.py           # Task request/response schemas
│   └── core/
│       ├── config.py         # Environment variable settings
│       ├── database.py       # MongoDB connection via Motor + Beanie
│       ├── security.py       # Password hashing, JWT creation/verification
│       └── dependencies.py   # FastAPI dependencies (get_current_user)
├── .env                      # Environment variables (never commit this)
├── .gitignore
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- MongoDB Atlas account (free tier works)
- Redis (via WSL on Windows: `sudo service redis-server start`)
- Resend account for email (free tier works)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/task-manager-api.git
cd task-manager-api
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
MONGODB_URL=mongodb+srv://<user>:<password>@cluster.mongodb.net/taskmanager?appName=Cluster0
DATABASE_NAME=taskmanager
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
RESEND_API_KEY=your_resend_api_key_here
```

### 5. Start Redis (Windows WSL)

```bash
wsl
sudo service redis-server start
```

### 6. Run the FastAPI server

```bash
uvicorn app.main:app --reload
```

### 7. Run the Celery worker (new terminal)

```bash
celery -A app.celery_app.celery worker --loglevel=info --pool=solo
```

---

## API Reference

### Auth

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and receive JWT tokens | No |

### Tasks

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/tasks/` | Get all tasks (paginated, filterable) | Yes |
| GET | `/tasks/{id}` | Get a single task by ID | Yes |
| POST | `/tasks/` | Create a new task | Yes |
| PUT | `/tasks/{id}` | Update a task | Yes |
| DELETE | `/tasks/{id}` | Delete a task | Yes |

### Query Parameters for GET /tasks/

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | int | 1 | Page number |
| `limit` | int | 10 | Results per page |
| `status_filter` | string | null | Filter by status (`pending`, `in_progress`, `completed`) |
| `priority_filter` | string | null | Filter by priority (`low`, `medium`, `high`) |

---

## Authentication Flow

```
POST /auth/register  →  creates user, returns user details
POST /auth/login     →  returns access_token + refresh_token
GET  /tasks/         →  requires header: Authorization: Bearer <access_token>
```

---

## Background Jobs

When a task is created, a Celery job is fired immediately:

```
POST /tasks/
    ↓
Task saved to MongoDB  →  201 response returned to client (instant)
    ↓
Celery picks up job from Redis queue (background)
    ↓
Resend API sends email notification to user
```

The client never waits for the email — it receives the response instantly.

---

## Interactive Docs

Once the server is running, visit:

- **Swagger UI** → `http://127.0.0.1:8000/docs`
- **ReDoc** → `http://127.0.0.1:8000/redoc`

---

## Environment Variables

| Variable | Description |
|---|---|
| `MONGODB_URL` | MongoDB Atlas connection string |
| `DATABASE_NAME` | MongoDB database name |
| `SECRET_KEY` | Secret key for JWT signing |
| `ALGORITHM` | JWT algorithm (HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime in minutes |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime in days |
| `RESEND_API_KEY` | Resend API key for sending emails |

---

## License

MIT
