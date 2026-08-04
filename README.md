# CampusPulse

> Discover. Connect. Explore.

CampusPulse is a full-stack web application that helps students discover, review, and share useful places around campus — cafeterias, libraries, gyms, and more. Students can browse and search approved places, write reviews, bookmark favorites, and plan visits. Admins moderate the platform by approving or rejecting submitted places and managing categories.

The backend is a Flask REST API (PostgreSQL, JWT authentication, role-based authorization). The frontend is a React single-page application built with Vite. The two are entirely separate applications that communicate only over HTTP — see [`INTEGRATION.md`](INTEGRATION.md) for a deep dive into exactly how they connect.

---

## Features

- JWT authentication (register/login) with hashed passwords
- Role-based authorization — student vs. admin
- Browse, search, and filter places by category
- Reviews and star ratings, with average rating shown per place
- Bookmarks (save places for later)
- Visit Plans (plan a visit, track status: Planned / Visited / Cancelled)
- Admin moderation — approve or reject submitted places, manage categories
- User profiles (bio, course, year of study, avatar, phone)
- Pagination on place listings
- Protected routes and role-gated pages on the frontend
- Loading, error, and empty states on every data-driven page

---

## Technology Stack

### Backend
- Python, Flask, Flask-RESTful
- Flask-SQLAlchemy (ORM)
- Flask-Migrate (Alembic migrations)
- Flask-JWT-Extended (authentication)
- Flask-CORS
- SQLAlchemy-Serializer
- python-dotenv
- Gunicorn (production server)

### Frontend
- React + Vite
- React Router
- Fetch API (no Axios)
- React Context API (auth state)
- Plain CSS (Flexbox/Grid, no UI framework)

### Database
- PostgreSQL

### Deployment
- Backend + Database → Render
- Frontend → Vercel

---

## Database Design

CampusPulse demonstrates all three relational database relationship types:

**One-to-One**
- `User` ↔ `Profile`

**One-to-Many**
- `Category` → `Places`
- `User` → `Reviews`
- `User` → submitted `Places`
- `User` (admin) → approved `Places`

**Many-to-Many** — implemented two different ways, deliberately:
- `User` ↔ `Place` through **`VisitPlan`** — an **association object**, because it carries its own data (`status`, `planned_date`, `visited_at`, `notes`) beyond just the two foreign keys.
- `User` ↔ `Place` through **`Bookmark`** — a plain join table, because a bookmark has no data of its own beyond "this user saved this place."

---

## Folder Structure

```
CAMPUSPULSE/
├── backend/
│   ├── app/
│   │   ├── __init__.py        # application factory
│   │   ├── config.py          # Config class, reads from .env
│   │   ├── extensions.py      # db, migrate, jwt, cors, api instances
│   │   ├── models/            # SQLAlchemy models (7 tables)
│   │   ├── resources/         # Flask-RESTful API endpoints
│   │   ├── services/          # business logic (e.g. review stats aggregation)
│   │   └── utils/             # pagination, decorators, error handlers, password hashing
│   ├── migrations/            # Alembic migration history
│   ├── seed.py                # sample data script
│   ├── run.py                 # entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/                # fetch-based API client
│   │   ├── context/            # AuthContext
│   │   ├── hooks/               # useAuth
│   │   ├── components/          # Navbar, ProtectedRoute, PlaceCard, etc.
│   │   ├── pages/                # one component per route
│   │   ├── App.jsx               # routes
│   │   └── main.jsx               # entry point
│   ├── vercel.json
│   └── package.json
├── render.yaml
└── README.md
```

---

## Installation

Clone the repo, then set up each half separately.

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

---

## Environment Variables

Neither `.env` file is committed — copy the example file on each side and fill in real values.

### Backend — `backend/.env` (copy from `backend/.env.example`)

```
FLASK_APP=run.py
FLASK_ENV=development

SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

DATABASE_URL=postgresql://username:password@localhost:5432/campuspulse_db

FRONTEND_URL=http://localhost:5173
```

`FRONTEND_URL` controls CORS — it restricts which origin is allowed to call the API. Locally it can be left as-is; in production it must be set to your real Vercel URL.

### Frontend — `frontend/.env` (copy from `frontend/.env.example`)

```
VITE_API_URL=http://127.0.0.1:5000
```

In production (Vercel), this is set in the project's dashboard instead of a committed file, pointing at your live Render backend URL.

---

## Database Setup

Create a local PostgreSQL database and a role for the app to use:

```bash
sudo -u postgres psql
CREATE DATABASE campuspulse_db;
CREATE USER campuspulse_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE campuspulse_db TO campuspulse_user;
\c campuspulse_db
GRANT ALL ON SCHEMA public TO campuspulse_user;
ALTER DATABASE campuspulse_db OWNER TO campuspulse_user;
\q
```

Then set `DATABASE_URL` in `backend/.env` to match, e.g.:
```
DATABASE_URL=postgresql://campuspulse_user:yourpassword@localhost:5432/campuspulse_db
```

---

## Migrations

Schema changes are tracked with Flask-Migrate (Alembic), not `db.create_all()` — this keeps the database schema versioned and reproducible, including in production.

```bash
cd backend
source .venv/bin/activate
flask db upgrade
```

This creates all 7 tables (`users`, `profiles`, `categories`, `places`, `reviews`, `visit_plans`, `bookmarks`) plus their foreign keys and constraints. If you change a model later, generate a new migration with:
```bash
flask db migrate -m "describe the change"
flask db upgrade
```

---

## Seeding

Populate the database with sample data for testing:

```bash
python seed.py
```

This creates:

| Username | Password | Role |
|---|---|---|
| `admin` | `admin123` | admin |
| `superadmin` | `password123` | admin |
| `jane_doe`, `john_smith`, `alice_wanjiru`, `brian_kiptoo`, `faith_njeri`, `kevin_otieno`, `grace_cherono`, `daniel_kamau` | `password123` | student |

...plus 8 categories, 24 places (20 approved, 3 pending, 1 rejected), 40 reviews, 20 visit plans, and 22 bookmarks — enough data to demonstrate pagination, search, filtering, and the review aggregation query meaningfully rather than on a handful of rows. Running `seed.py` again clears existing data first, so it's safe to re-run any time.

---

## Running the Backend

```bash
cd backend
source .venv/bin/activate
python run.py
```

Runs at `http://127.0.0.1:5000`. Visit it directly for a welcome message, or `http://127.0.0.1:5000/api/categories` to confirm seeded data is reachable.

---

## Running the Frontend

```bash
cd frontend
npm run dev
```

Runs at `http://localhost:5173`. The backend must be running for any page beyond the static shell to work.

---

## API Endpoints

All routes are prefixed `/api`, return JSON, and errors follow the shape `{"error": "message"}`.

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | — | Create an account |
| POST | `/auth/login` | — | Log in, returns a JWT |
| GET | `/auth/me` | Required | Current user's data |
| GET | `/categories` | — | List categories |
| POST | `/categories` | Admin | Create a category |
| GET | `/categories/:id` | — | Get one category |
| PUT | `/categories/:id` | Admin | Update a category |
| DELETE | `/categories/:id` | Admin | Delete a category |
| GET | `/places` | — | List approved places (supports `page`, `per_page`, `category_id`, `search`) |
| POST | `/places` | Required | Submit a new place (status: Pending) |
| GET | `/places/:id` | — | Get one place, with review stats |
| PUT | `/places/:id` | Owner/Admin | Update a place |
| DELETE | `/places/:id` | Owner/Admin | Delete a place |
| GET | `/places/mine` | Required | Places you submitted |
| GET | `/places/pending` | Admin | Pending submissions queue |
| POST | `/places/:id/approve` | Admin | Approve a place |
| POST | `/places/:id/reject` | Admin | Reject a place |
| GET | `/places/:id/reviews` | — | List reviews for a place |
| POST | `/places/:id/reviews` | Required | Post a review (rating 1–5) |
| PUT | `/reviews/:id` | Owner | Edit your review |
| DELETE | `/reviews/:id` | Owner/Admin | Delete a review |
| GET | `/visit-plans` | Required | Your visit plans |
| POST | `/visit-plans` | Required | Create a visit plan |
| PUT | `/visit-plans/:id` | Owner | Update status/notes |
| DELETE | `/visit-plans/:id` | Owner | Cancel a visit plan |
| GET | `/bookmarks` | Required | Your bookmarks |
| POST | `/bookmarks` | Required | Bookmark a place |
| DELETE | `/bookmarks/:id` | Owner | Remove a bookmark |
| GET | `/profile` | Required | Your profile |
| PUT | `/profile` | Required | Update your profile |

---

## Deployment

**Backend (Render):** `render.yaml` at the repo root defines the web service and PostgreSQL database. Connect the GitHub repo on Render, let it detect the Blueprint, and set `SECRET_KEY`/`JWT_SECRET_KEY` (auto-generated) and `FRONTEND_URL` (your Vercel URL) as environment variables. The start command runs `flask db upgrade` before starting the server, so migrations apply automatically on every deploy.

**Frontend (Vercel):** set the **Root Directory** to `frontend`, and add an environment variable `VITE_API_URL` pointing at your live Render backend URL. `frontend/vercel.json` adds the rewrite rule React Router needs so page refreshes on routes like `/places/5` don't 404.

Deploy the backend first (you need its URL for the frontend's env var), then the frontend, then go back and set `FRONTEND_URL` on the backend to the frontend's real URL and redeploy.

---

## Future Enhancements

- JWT refresh tokens (access tokens currently expire after 15 minutes with no renewal flow)
- Rate limiting on authentication endpoints
- A dedicated "is this place bookmarked" endpoint instead of checking client-side over the full list
- Automated test suite
- Image upload instead of raw image URLs

---

## Contributors

- **Charity Jepkoech** — full-stack development student

