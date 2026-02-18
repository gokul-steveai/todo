# To-Do API

A simple To-Do API built with FastAPI, featuring user authentication and CRUD operations for managing tasks.

## Features

- User registration and authentication with JWT tokens
- Create, read, update, and delete to-do items
- Task status management (pending, in progress, completed)
- User-specific to-do lists
- Password hashing with Argon2

## Tech Stack

- **FastAPI** - Modern web framework
- **SQLModel** - SQL database ORM
- **SQLite** - Database
- **JWT** - Token-based authentication
- **Argon2** - Password hashing

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Interactive API docs available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT token

### To-Do Operations

All endpoints require Bearer token authentication.

- `GET /todos` - Get all to-dos (supports filtering by status, pagination)
- `POST /todos` - Create a new to-do
- `PUT /todos/{todo_id}` - Update to-do status
- `POST /todos/{todo_id}/toggle` - Toggle completion status
- `DELETE /todos/{todo_id}` - Delete a to-do

## Project Structure

```
todo/
├── main.py              # Application entry point
├── utils.py             # Authentication & utility functions
├── models/
│   ├── connect.py       # Database connection
│   ├── todo.py          # Todo model
│   └── user.py          # User model
├── routers/
│   ├── auth.py          # Authentication routes
│   └── todo.py          # Todo routes
└── schemas/
    ├── auth.py          # Auth request/response schemas
    ├── todo.py          # Todo schemas
    └── user.py          # User schemas
```

## Usage Example

1. Register a user:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","full_name":"John Doe"}'
```

2. Login:
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

3. Create a to-do (use token from login):
```bash
curl -X POST "http://localhost:8000/todos" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries","description":"Milk, Bread, Eggs"}'
```

## Environment

The application uses SQLite by default. Database file `database.db` is created automatically on startup.

## Security

- Passwords are hashed using Argon2
- JWT tokens expire after 30 minutes
- Bearer token authentication required for protected routes
