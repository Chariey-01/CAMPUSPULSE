# CampusPulse

> Discover. Connect. Explore.

CampusPulse is a full-stack web application designed to help students discover, review, and share useful locations around campus. The platform enables students to explore restaurants, transport services, banks, health facilities, shopping areas, study spots, and hidden gems while allowing administrators to moderate community submissions.

-----------------------------------------------------------------------------------------------------------------------------------------------------

## Features

- JWT Authentication & Authorization
- Student and Admin Roles
- User Profiles
- Browse Places by Category
- Search and Filter
- Reviews & Ratings
- Visit Planner
- Bookmarks
- Admin Moderation
- Pagination
- Deep SQL Queries
- Responsive React Interface

-----------------------------------------------------------------------------------------------------------------------------------------------------

## Technology Stack

### Frontend

- React (Vite)
- JavaScript
- React Router
- Fetch API
- React Context
- CSS

### Backend

- Python
- Flask
- Flask-RESTful
- Flask-JWT-Extended
- Flask-SQLAlchemy
- Flask-Migrate
- SQLAlchemy-Serializer

### Database

- PostgreSQL

### Deployment

- Frontend: Vercel
- Backend: Render
- Database: PostgreSQL on Render

-----------------------------------------------------------------------------------------------------------------------------------------------------

## Database Relationships

- One-to-One
  - User → Profile

- One-to-Many
  - Category → Places
  - User → Reviews
  - Place → Reviews

- Many-to-Many
  - User ↔ Place (Visit Plans)

-----------------------------------------------------------------------------------------------------------------------------------------------------

## Installation

### Backend

```bash
cd backend

python -m venv . / pipenv install

source .venv/bin/activate or pipenv shell

pip install -r requirements.txt

flask db upgrade

python3 seed.py

python3 app.py
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

-----------------------------------------------------------------------------------------------------------------------------------------------------

## Environment Variables

```
DATABASE_URL=

JWT_SECRET_KEY=

SECRET_KEY=
```

-----------------------------------------------------------------------------------------------------------------------------------------------------

## API

The backend exposes a REST API secured with JWT authentication.

