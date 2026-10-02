# Krishi Drishti

Krishi Drishti is a full-stack AI-powered agricultural advisory platform for Indian farmers. It combines a React frontend, FastAPI backend, PostgreSQL database, OTP authentication, geolocation support, soil-health data handling, multilingual UI, crop recommendations, and yield-planning workflows.

## Table of Contents

- [Project Overview](#project-overview)
- [Main Features](#main-features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Frontend Documentation](#frontend-documentation)
- [Backend Documentation](#backend-documentation)
- [Database Documentation](#database-documentation)
- [Authentication Flow](#authentication-flow)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Testing the OTP Flow](#testing-the-otp-flow)
- [Troubleshooting](#troubleshooting)
- [Security Notes](#security-notes)
- [Future Improvements](#future-improvements)
- [Development Checklist](#development-checklist)

## Project Overview

Krishi Drishti helps farmers register with OTP, store farm details, capture geolocation, upload soil-health data, and receive crop recommendations, yield plans, and optimization advice based on soil, weather, and farm context.

The repository is organized as a frontend-backend monorepo:

- The **frontend** is a React single-page application.
- The **backend** is a FastAPI service.
- **PostgreSQL** stores persistent data.
- **PostGIS** supports spatial farm location data.

## Main Features

- Phone-number registration and login using OTP.
- Registration and login use the same OTP flow with different purposes.
- Multilingual UI with a shared language selector.
- Farm onboarding and geolocation capture.
- Soil health card data support.
- Crop recommendation and yield planning modules.
- PostgreSQL persistence with relational schema.
- PostGIS support for geospatial farm points.
- FastAPI auto-generated documentation.
- Modular frontend and backend architecture.

## Technology Stack

### Frontend

- React
- React Router
- Axios
- React Toastify
- React i18next
- i18next
- CSS
- Create React App and `react-scripts`

### Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- GeoAlchemy2
- PostgreSQL driver
- Twilio SDK

### Database and services

- PostgreSQL
- PostGIS
- Twilio SMS
- Weather API provider
- data.gov.in datasets
- Browser geolocation API

## System Architecture

```text
┌─────────────────────────┐
│        React UI         │
│  Login, Register, OTP   │
│ Dashboard, Onboarding   │
└────────────┬────────────┘
             │ HTTP / JSON
             ▼
┌─────────────────────────┐
│      FastAPI API        │
│ Auth, Farm, Recommend   │
│ Plan and Weather APIs   │
└────────────┬────────────┘
             │ SQLAlchemy
             ▼
┌─────────────────────────┐
│       PostgreSQL        │
│ Users, Farms, Soil Data │
│ Crops, Plans, Weather   │
└─────────────────────────┘
```

## Project Structure

```text
krishi-drishti/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── otp.py
│   │   │   ├── farm.py
│   │   │   └── ...
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── farm.py
│   │   │   ├── recommend.py
│   │   │   └── plan.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   └── ...
│   │   └── services/
│   │       └── sms.py
│   ├── database/
│   │   ├── init.sql
│   │   └── seed_data.sql
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── robots.txt
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.js
│   │   ├── App.css
│   │   ├── components/
│   │   │   ├── Auth/
│   │   │   │   ├── Login.jsx
│   │   │   │   ├── Register.jsx
│   │   │   │   ├── VerifyOTP.jsx
│   │   │   │   └── Auth.css
│   │   │   ├── Dashboard/
│   │   │   ├── Onboarding/
│   │   │   └── shared/
│   │   │       ├── LanguageSelector.jsx
│   │   │       └── LoadingSpinner.jsx
│   │   ├── hooks/
│   │   │   └── useGeolocation.jsx
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── geolocation.js
│   │   └── i18n/
│   │       └── config.js
│   ├── package.json
│   └── .env
├── docker-compose.yml
└── README.md
```

## Frontend Documentation

### `src/App.jsx`

Defines React routes, public pages, protected pages, redirects, lazy-loaded components, and global toast notifications.

Public routes include:

```text
/
/register
/login
/verify-otp
```

Protected routes may include:

```text
/onboarding/location
/onboarding/shc-upload
/onboarding/farm-details
/dashboard
/dashboard/crop-recommendation
/dashboard/yield-plan
```

### `Register.jsx`

Handles new-user registration. It collects the country code and phone number, validates the input, calls `/auth/send-otp` with `purpose: "registration"`, and navigates to OTP verification.

### `Login.jsx`

Handles existing-user login. It calls the same OTP endpoint with `purpose: "login"`.

### `VerifyOTP.jsx`

Accepts the OTP, calls `/auth/verify-otp`, displays success or failure messages, and redirects after verification.

### `Auth.css`

Contains shared authentication styles for cards, fields, OTP controls, buttons, footer links, responsive layouts, and phone-input sizing.

### `LanguageSelector.jsx`

Changes the active language through i18next. It should be rendered inside pages such as `Register.jsx` and `Login.jsx`, not registered as a route.

### `useGeolocation.jsx`

Provides `location`, `error`, `loading`, and `getLocation()` for farm-location capture. `useEffect` is not required when location is requested manually.

### `services/api.js`

Centralizes Axios calls to the FastAPI backend, including OTP sending and verification.

## Backend Documentation

### `app/main.py`

Creates the FastAPI app, configures CORS, registers routers, and provides health endpoints.

The following line is required:

```python
app.include_router(auth.router)
```

### `app/config.py`

Loads the database URL, secret key, debug settings, environment, and Twilio credentials from `.env`.

### `app/database.py`

Creates the SQLAlchemy engine, session factory, declarative base, and `get_db()` dependency.

### `app/routers/auth.py`

Provides:

- `POST /auth/send-otp`
- `POST /auth/verify-otp`

The router must use:

```python
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
```

### `app/services/sms.py`

Sends OTPs through Twilio in production. Development mode may print OTPs to the backend console.

### Models and other routers

- `models/user.py`: user table model.
- `models/otp.py`: OTP table model.
- `models/farm.py`: farm and soil-related models.
- `routers/farm.py`: farm operations.
- `routers/recommend.py`: crop recommendations.
- `routers/plan.py`: yield plans and optimization actions.

## Database Documentation

### Main tables

- `users`: Registered users and verification state.
- `otp_codes`: OTP values, expiry, purpose, and verification state.
- `farms`: Farm metadata and location.
- `soil_health_cards`: Soil nutrient and health-card data.
- `crop_master`: Crop catalog.
- `crop_recommendations`: Farm-specific crop recommendations.
- `yield_plans`: Baseline and optimized yield calculations.
- `optimization_recommendations`: Recommended actions.
- `weather_cache`: Cached weather and forecasts.

### Database scripts

- `database/init.sql`: Creates the PostGIS extension, tables, indexes, and triggers.
- `database/seed_data.sql`: Inserts initial crop data.

### Enable PostGIS

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
SELECT PostGIS_Version();
```

PostGIS must be installed on the same PostgreSQL system before this SQL command can succeed.

## Authentication Flow

1. The user enters a phone number.
2. The frontend sends a request to `/auth/send-otp`.
3. The backend generates and stores an OTP.
4. Twilio sends the OTP, or development mode prints it.
5. The user enters the OTP.
6. The frontend sends it to `/auth/verify-otp`.
7. The backend validates expiration, value, and purpose.
8. Registration creates or verifies a user.
9. Login requires an existing verified user.
10. The frontend redirects the user after success.

Registration request:

```json
{
  "phone": "9876543210",
  "country_code": "+91",
  "purpose": "registration"
}
```

Verification request:

```json
{
  "phone": "9876543210",
  "country_code": "+91",
  "otp_code": "123456",
  "purpose": "registration"
}
```

## API Documentation

Start the backend and open:

```text
http://127.0.0.1:8000/docs
```

Alternative documentation:

```text
http://127.0.0.1:8000/redoc
```

### System endpoints

- `GET /`
- `GET /health`

### Authentication endpoints

- `POST /auth/send-otp`
- `POST /auth/verify-otp`
- `GET /auth/test` if retained

## Environment Variables

### Backend `.env`

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/krishi_drishti
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
DEBUG=True
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

### Frontend `.env`

```env
REACT_APP_API_URL=http://127.0.0.1:8000
REACT_APP_ENVIRONMENT=development
```

Restart the frontend after changing its `.env` file.

## Installation

### Prerequisites

- Python 3.11 or compatible.
- Node.js and npm.
- PostgreSQL.
- PostGIS.
- Git.
- Optional: Docker Desktop.
- Optional: Twilio account.

### Backend installation

```bash
cd D:\krishi-drishti\backend
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If required, install packages explicitly:

```bash
python -m pip install fastapi uvicorn sqlalchemy
python -m pip install psycopg2-binary geoalchemy2
python -m pip install pydantic-settings twilio
```

### Frontend installation

```bash
cd D:\krishi-drishti\frontend
npm install
```

If `react-scripts` is missing:

```bash
npm install react-scripts@5.0.1
```

## Database Setup

1. Open pgAdmin.
2. Create a database named `krishi_drishti`.
3. Open Query Tool for that database.
4. Enable PostGIS.
5. Execute `database/init.sql`.
6. Execute `database/seed_data.sql`.

Using `psql`:

```bash
cd D:\krishi-drishti\backend
psql -U postgres -d krishi_drishti -f database\init.sql
psql -U postgres -d krishi_drishti -f database\seed_data.sql
```

Verify tables:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

Verify crops:

```sql
SELECT COUNT(*) FROM crop_master;
```

## Running the Project

Only two terminals are required if PostgreSQL is already running as a Windows service.

### Terminal 1: Backend

```bash
cd D:\krishi-drishti\backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000
```

Backend URL:

```text
http://127.0.0.1:8000
```

### Terminal 2: Frontend

```bash
cd D:\krishi-drishti\frontend
npm start
```

Frontend URL:

```text
http://localhost:3000
```

Docker is optional unless you want to run services in containers.

## Testing the OTP Flow

### Registration

1. Open `http://localhost:3000/register`.
2. Enter a phone number.
3. Click the registration OTP button.
4. Check the backend terminal or phone for the OTP.
5. Enter the OTP.
6. Verify the user in the `users` table.

### Login

1. Open `http://localhost:3000/login`.
2. Enter a registered phone number.
3. Request an OTP.
4. Enter the OTP.
5. Continue to the dashboard.

## Troubleshooting

### `POST /auth/send-otp 404 Not Found`

Check that:

```python
app.include_router(auth.router)
```

exists in `main.py`, that `auth.py` uses the `/auth` prefix, and that `/auth/send-otp` appears in `/docs`.

### `ModuleNotFoundError: twilio`

```bash
python -m pip install twilio
python -c "import twilio; print(twilio.__version__)"
```

Use the same Python environment to install the package and run Uvicorn.

### `ModuleNotFoundError: geoalchemy2`

```bash
python -m pip install geoalchemy2
```

### `ModuleNotFoundError: psycopg2`

```bash
python -m pip install psycopg2-binary
```

### `constr()` does not accept `regex`

For Pydantic v2, use `Field(pattern=...)` instead of `regex=`.

### `react-scripts` is not recognized

```bash
cd D:\krishi-drishti\frontend
npm install
npm install react-scripts@5.0.1
```

### Missing `public/index.html`

Create `frontend/public/index.html` with:

```html
<div id="root"></div>
```

### Language selector does not work

Check that:

- i18next is installed.
- The i18n configuration is imported in `index.js`.
- `LanguageSelector` calls `i18n.changeLanguage()`.
- Translation keys exist.
- The frontend was restarted after configuration changes.

### Login link does not navigate

Use React Router:

```jsx
import { Link } from 'react-router-dom';

<Link to="/login">Login with OTP</Link>
```

### CORS errors

Allow the React origins in FastAPI:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

## Security Notes

Never commit these values to a public repository:

- Twilio Account SID.
- Twilio Auth Token.
- Database password.
- JWT secret.
- Weather API key.
- data.gov.in API key.

Add the following to `.gitignore`:

```gitignore
.env
venv/
node_modules/
__pycache__/
*.pyc
```

For production, also implement:

- Hashed OTP storage.
- OTP rate limiting.
- OTP attempt limits.
- Resend cooldown.
- HTTPS.
- Secure JWT handling.
- Database migrations.
- Backups and monitoring.

## Future Improvements

- JWT access and refresh tokens.
- Resend OTP countdown.
- Voice input and text-to-speech.
- Offline PWA support.
- Regional-language voice support.
- ML-based crop recommendation.
- Yield prediction.
- Irrigation recommendation.
- Fertilizer recommendation.
- Pest and disease prediction.
- Mandi price analysis.
- Government scheme information.
- Docker deployment.
- CI/CD and production monitoring.

## Development Checklist

### Backend

- [ ] PostgreSQL is running.
- [ ] `krishi_drishti` database exists.
- [ ] PostGIS is enabled.
- [ ] `init.sql` succeeded.
- [ ] `seed_data.sql` succeeded.
- [ ] Virtual environment is active.
- [ ] Dependencies are installed.
- [ ] `.env` is configured.
- [ ] Twilio is installed.
- [ ] `/auth/send-otp` appears in Swagger.
- [ ] `/auth/verify-otp` appears in Swagger.
- [ ] Backend starts on port `8000`.

### Frontend

- [ ] `npm install` completed.
- [ ] `react-scripts` is installed.
- [ ] `public/index.html` exists.
- [ ] `src/index.js` exists.
- [ ] Routes are present in `App.jsx`.
- [ ] Frontend `.env` is configured.
- [ ] Language selector is rendered.
- [ ] Registration page works.
- [ ] Login page works.
- [ ] OTP page works.
- [ ] Frontend starts on port `3000`.

### Authentication

- [ ] Registration request reaches backend.
- [ ] OTP is stored in `otp_codes`.
- [ ] Twilio sends SMS or development mode prints OTP.
- [ ] OTP verification succeeds.
- [ ] User is created in `users`.
- [ ] Login rejects unregistered users.
- [ ] Login succeeds for registered users.

## Useful Commands

Start backend:

```bash
cd D:\krishi-drishti\backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000
```

Start frontend:

```bash
cd D:\krishi-drishti\frontend
npm start
```

Inspect FastAPI routes:

```bash
python
```

```python
from app.main import app

for route in app.routes:
    print(route.path, route.methods)
```

Inspect users:

```sql
SELECT id, phone, country_code, is_verified
FROM users;
```

Inspect OTP records:

```sql
SELECT id, phone, purpose, is_verified, expires_at
FROM otp_codes
ORDER BY created_at DESC;
```

## Conclusion

Krishi Drishti separates the user interface, API, business logic, and database layers. The React frontend manages interaction and navigation, FastAPI handles application logic, PostgreSQL stores persistent records, PostGIS supports farm location data, and Twilio provides OTP delivery.

For normal local development, run PostgreSQL as a Windows service and use two terminals:

```text
Terminal 1: FastAPI backend
Terminal 2: React frontend
```

Application URLs:

- Frontend: `http://localhost:3000`
- Backend: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`
