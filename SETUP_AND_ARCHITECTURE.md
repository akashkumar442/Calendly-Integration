# Appointment Scheduling Agent - Complete Setup & Architecture Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Project Setup](#project-setup)
4. [Project Structure](#project-structure)
5. [Component Interconnections](#component-interconnections)
6. [Implementation Details](#implementation-details)
7. [API Implementation](#api-implementation)
8. [Business Logic](#business-logic)
9. [Data Models](#data-models)
10. [Testing](#testing)

---

## Project Overview

This is a **Medical Appointment Scheduling Agent** that simulates a Calendly-like scheduling system. It provides a RESTful API for checking doctor availability and booking appointments. The system is a mock implementation that doesn't require external services or databases - all data is loaded from JSON files and runtime bookings are stored in-memory.

### Key Features
- Check available appointment slots for a given date and appointment type
- Book appointments with patient information
- Conflict detection to prevent double-booking
- Support for multiple appointment types with different durations
- Working hours management based on weekdays
- Runtime booking management (in-memory)

---

## Tech Stack

### Core Technologies

1. **Python 3.10+**
   - Primary programming language
   - Used for backend API development

2. **FastAPI 0.114.2**
   - Modern, fast web framework for building APIs
   - Automatic API documentation (Swagger/OpenAPI)
   - Built-in data validation using Pydantic
   - Async support
   - Type hints support

3. **Uvicorn 0.30.6**
   - ASGI server for running FastAPI applications
   - High-performance async server
   - Hot-reload support for development

4. **Pydantic 2.9.2**
   - Data validation using Python type annotations
   - Automatic serialization/deserialization
   - Schema generation for API documentation
   - Email validation support

5. **Python-dateutil 2.9.0.post0**
   - Date and time parsing utilities
   - Enhanced datetime operations

6. **Email-validator 2.1.1**
   - Email format validation
   - Used by Pydantic for EmailStr type

### Development & Testing Tools

7. **Pytest 8.3.3**
   - Testing framework
   - Test discovery and execution
   - Assertion utilities

8. **HTTPX 0.27.2**
   - HTTP client library
   - Used by FastAPI TestClient for testing
   - Async HTTP requests support

---

## Project Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment tool (venv)

### Step-by-Step Setup Instructions

#### 1. Clone/Navigate to Project Directory
```bash
cd appointment-scheduling-agent
```

#### 2. Create Virtual Environment
**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- fastapi==0.114.2
- uvicorn==0.30.6
- pydantic==2.9.2
- email-validator==2.1.1
- python-dateutil==2.9.0.post0
- pytest==8.3.3
- httpx==0.27.2

#### 4. Verify Installation
```bash
python --version  # Should show Python 3.10+
pip list  # Should show all installed packages
```

#### 5. Run the Application

**Option A: From project root**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Option B: Using absolute path**
```bash
uvicorn backend.main:app --reload --port 8000 --app-dir /path/to/appointment-scheduling-agent
```

#### 6. Access the Application
- **API Base URL:** `http://localhost:8000`
- **Interactive API Docs (Swagger):** `http://localhost:8000/docs`
- **Alternative API Docs (ReDoc):** `http://localhost:8000/redoc`
- **Health Check:** `http://localhost:8000/health`

---

## Project Structure

```
appointment-scheduling-agent/
│
├── backend/                    # Main application code
│   ├── __init__.py            # Python package marker
│   ├── main.py                # FastAPI application entry point
│   │
│   ├── api/                   # API route handlers
│   │   ├── __init__.py
│   │   └── calendly_integration.py  # Calendly API endpoints
│   │
│   └── models/                # Data models and schemas
│       ├── __init__.py
│       └── schemas.py         # Pydantic models for request/response
│
├── data/                      # Data storage
│   └── doctor_schedule.json   # Doctor working hours and existing bookings
│
├── tests/                     # Test files
│   └── test_agent.py          # Unit and integration tests
│
├── requirements.txt           # Python dependencies
├── README.md                  # Basic project documentation
└── SETUP_AND_ARCHITECTURE.md  # This comprehensive documentation
```

### File Responsibilities

#### `backend/main.py`
- FastAPI application initialization
- Router registration
- Health check endpoint
- Application configuration

#### `backend/api/calendly_integration.py`
- API endpoint definitions
- Business logic for availability checking
- Booking management logic
- Slot generation algorithms
- Conflict detection

#### `backend/models/schemas.py`
- Pydantic data models
- Request/response schemas
- Data validation rules
- Type definitions

#### `data/doctor_schedule.json`
- Doctor working hours (per weekday)
- Pre-existing bookings
- Static schedule data

#### `tests/test_agent.py`
- Unit tests for endpoints
- Integration tests for booking flow
- Health check tests

---

## Component Interconnections

### Architecture Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Client (HTTP Request)                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│                    (backend/main.py)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI App Instance                                 │  │
│  │  - Registers routers                                  │  │
│  │  - Health check endpoint                              │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Calendly Integration Router                     │
│         (backend/api/calendly_integration.py)               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  GET /api/calendly/availability                       │  │
│  │  POST /api/calendly/book                              │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────┬──────────────────────────┬───────────────────┘
               │                          │
               ▼                          ▼
┌──────────────────────────┐  ┌──────────────────────────────┐
│   Pydantic Schemas       │  │   Business Logic Functions   │
│  (backend/models/        │  │  - _load_schedule()          │
│   schemas.py)            │  │  - _generate_slots()         │
│  - Request validation    │  │  - _collect_existing_        │
│  - Response models       │  │    bookings()                │
│  - Data serialization    │  │  - _overlaps()               │
│                          │  │  - _get_weekday()            │
└──────────────────────────┘  └──────────┬───────────────────┘
                                         │
                                         ▼
                          ┌──────────────────────────────┐
                          │   Data Sources               │
                          │  - doctor_schedule.json      │
                          │  - RUNTIME_BOOKINGS (dict)   │
                          └──────────────────────────────┘
```

### Data Flow

1. **Request Flow:**
   - Client sends HTTP request → FastAPI receives request
   - FastAPI routes to appropriate endpoint → Router processes request
   - Router validates request using Pydantic schemas
   - Business logic functions execute
   - Data is loaded from JSON file and in-memory storage
   - Response is generated and validated using Pydantic
   - JSON response sent back to client

2. **Booking Flow:**
   - Availability check → Generate slots → Check conflicts
   - Booking request → Validate slot → Store in RUNTIME_BOOKINGS
   - Generate booking ID and confirmation code
   - Return booking confirmation

---

## Implementation Details

### 1. FastAPI Application Setup (`backend/main.py`)

```python
from fastapi import FastAPI
from backend.api.calendly_integration import router as calendly_router

app = FastAPI(title="Medical Appointment Scheduling Agent — Calendly Mock")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(calendly_router, prefix="/api/calendly", tags=["calendly"])
```

**Key Points:**
- Creates FastAPI application instance
- Registers health check endpoint
- Includes calendly router with `/api/calendly` prefix
- Automatic OpenAPI documentation generation

### 2. Data Models (`backend/models/schemas.py`)

**AppointmentType:**
- Literal type with 4 values: "consultation", "followup", "physical", "special"
- Ensures type safety at compile time

**Slot Model:**
- `start_time`: String in HH:MM format
- `end_time`: String in HH:MM format
- `available`: Boolean indicating slot availability

**Patient Model:**
- `name`: String
- `email`: EmailStr (validated email format)
- `phone`: String

**BookingRequest:**
- Validates incoming booking requests
- Includes appointment type, date, time, patient info, and optional reason

**BookingResponse:**
- Returns booking confirmation with ID, status, confirmation code, and details

### 3. Business Logic (`backend/api/calendly_integration.py`)

#### Key Functions:

**`_load_schedule()`**
- Loads `doctor_schedule.json` from data directory
- Returns dictionary with working hours and existing bookings
- Handles file not found errors

**`_get_weekday(date_str)`**
- Converts date string to weekday name
- Used to lookup working hours for specific day

**`_parse_time(date_str, time_str)`**
- Combines date and time strings into datetime object
- Format: "YYYY-MM-DD HH:MM"

**`_format_time(dt)`**
- Converts datetime to time string
- Format: "HH:MM"

**`_overlaps(a_start, a_end, b_start, b_end)`**
- Checks if two time ranges overlap
- Used for conflict detection
- Logic: `a_start < b_end and b_start < a_end`

**`_collect_existing_bookings(schedule_data, date_str)`**
- Collects bookings from two sources:
  1. Static bookings from JSON file
  2. Runtime bookings from RUNTIME_BOOKINGS dictionary
- Returns list of (start_datetime, end_datetime) tuples

**`_generate_slots(date_str, appointment_type)`**
- Core slot generation algorithm
- Steps:
  1. Load schedule data
  2. Get weekday and working hours
  3. Get appointment duration
  4. Collect existing bookings
  5. Generate candidate slots at duration intervals
  6. Check each slot for conflicts
  7. Mark slots as available/unavailable
  8. Return list of Slot objects

### 4. Runtime Booking Storage

```python
RUNTIME_BOOKINGS: Dict[str, List[Tuple[str, str]]] = {}
```

- In-memory dictionary storing bookings made during runtime
- Key: date string (YYYY-MM-DD)
- Value: List of (start_time, end_time) tuples
- **Note:** Bookings are lost on server restart (not persisted)

### 5. Appointment Durations

```python
APPOINTMENT_DURATIONS_MIN = {
    "consultation": 30,  # 30 minutes
    "followup": 15,      # 15 minutes
    "physical": 45,      # 45 minutes
    "special": 60,       # 60 minutes
}
```

---

## API Implementation

### Endpoint 1: GET `/api/calendly/availability`

**Purpose:** Retrieve available appointment slots for a given date and appointment type.

**Query Parameters:**
- `date` (required): Date in YYYY-MM-DD format
- `appointment_type` (required): One of "consultation", "followup", "physical", "special"

**Request Example:**
```bash
curl "http://localhost:8000/api/calendly/availability?date=2024-01-15&appointment_type=consultation"
```

**Response Structure:**
```json
{
  "date": "2024-01-15",
  "available_slots": [
    {
      "start_time": "09:00",
      "end_time": "09:30",
      "available": true
    },
    {
      "start_time": "09:30",
      "end_time": "10:00",
      "available": false
    },
    {
      "start_time": "10:00",
      "end_time": "10:30",
      "available": true
    }
  ]
}
```

**Implementation Logic:**
1. Validate date format (YYYY-MM-DD regex pattern)
2. Validate appointment_type against allowed values
3. Call `_generate_slots()` function
4. Return AvailabilityResponse with date and slots

**Error Handling:**
- 400: Invalid date format or appointment type
- 500: Schedule data file not found

### Endpoint 2: POST `/api/calendly/book`

**Purpose:** Book an appointment for a selected time slot.

**Request Body:**
```json
{
  "appointment_type": "consultation",
  "date": "2024-01-15",
  "start_time": "10:00",
  "patient": {
    "name": "Akash Kumar",
    "email": "akash@example.com",
    "phone": "+1-555-0100"
  },
  "reason": "Annual checkup"
}
```

**Request Example:**
```bash
curl -X POST http://localhost:8000/api/calendly/book \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_type": "consultation",
    "date": "2024-01-15",
    "start_time": "10:00",
    "patient": {
      "name": "Akash Kumar",
      "email": "akash@example.com",
      "phone": "+1-555-0100"
    },
    "reason": "Annual checkup"
  }'
```

**Response Structure:**
```json
{
  "booking_id": "APPT-20240115-A1B2C3D4",
  "status": "confirmed",
  "confirmation_code": "ABC123",
  "details": {
    "appointment_type": "consultation",
    "date": "2024-01-15",
    "start_time": "10:00",
    "end_time": "10:30",
    "patient": {
      "name": "Akash Kumar",
      "email": "akash@example.com",
      "phone": "+1-555-0100"
    },
    "reason": "Annual checkup"
  }
}
```

**Implementation Logic:**
1. Validate appointment_type
2. Parse and validate date/time format
3. Calculate end_time based on appointment duration
4. Generate available slots for the date
5. Check if requested slot exists and is available
6. If available:
   - Add booking to RUNTIME_BOOKINGS
   - Generate unique booking_id (format: APPT-YYYYMMDD-UUID8)
   - Generate confirmation_code (6-character uppercase)
   - Return BookingResponse with confirmation
7. If not available, return error

**Error Handling:**
- 400: Invalid appointment type, date/time format, or slot outside working hours
- 409: Requested time slot is no longer available (conflict)

### Endpoint 3: GET `/health`

**Purpose:** Health check endpoint to verify server is running.

**Response:**
```json
{
  "status": "ok"
}
```

---

## Business Logic

### Slot Generation Algorithm

1. **Load Schedule Data:**
   - Read `doctor_schedule.json`
   - Extract working hours for the requested weekday
   - If no working hours for that day, return empty slots

2. **Determine Appointment Duration:**
   - Lookup duration from `APPOINTMENT_DURATIONS_MIN` dictionary
   - Based on appointment_type

3. **Collect Existing Bookings:**
   - Load bookings from JSON file for the requested date
   - Load runtime bookings from `RUNTIME_BOOKINGS` dictionary
   - Convert all to datetime objects

4. **Generate Candidate Slots:**
   - Start from working hours start time
   - Create slots at duration intervals
   - For each slot:
     - Calculate start and end times
     - Check for overlaps with existing bookings
     - Mark as available (true) or unavailable (false)
   - Continue until slot end time exceeds working hours end time

5. **Return Slots:**
   - Format times as "HH:MM" strings
   - Return list of Slot objects

### Conflict Detection Logic

**Overlap Detection:**
Two time ranges overlap if:
```
a_start < b_end AND b_start < a_end
```

**Example:**
- Slot A: 09:00 - 09:30
- Booking B: 09:15 - 10:00
- Overlap: 09:00 < 10:00 AND 09:15 < 09:30 → TRUE (conflict)

### Booking Validation Logic

1. **Pre-booking Checks:**
   - Validate appointment_type exists
   - Validate date/time format
   - Calculate end_time based on duration

2. **Availability Check:**
   - Regenerate slots for the date (includes latest runtime bookings)
   - Check if requested slot exists in generated slots
   - Verify slot is marked as available

3. **Booking Creation:**
   - Add booking to RUNTIME_BOOKINGS dictionary
   - Generate unique identifiers
   - Return confirmation

### Working Hours Logic

- Working hours are defined per weekday in JSON file
- If a weekday has `null` working hours, no slots are generated
- Slots are only generated within working hours
- Example: Monday 09:00-17:00 means slots from 09:00 to 16:30 (last slot ends at 17:00)

---

## Data Models

### Request Models

**AvailabilityQuery:**
- Used internally for type hints
- Not directly used in endpoint (query parameters used instead)

**BookingRequest:**
```python
{
  "appointment_type": AppointmentType,
  "date": str,  # YYYY-MM-DD
  "start_time": str,  # HH:MM
  "patient": Patient,
  "reason": Optional[str]
}
```

### Response Models

**AvailabilityResponse:**
```python
{
  "date": str,
  "available_slots": List[Slot]
}
```

**Slot:**
```python
{
  "start_time": str,  # HH:MM
  "end_time": str,    # HH:MM
  "available": bool
}
```

**BookingResponse:**
```python
{
  "booking_id": str,
  "status": Literal["confirmed", "failed"],
  "confirmation_code": str,
  "details": BookingDetails
}
```

**BookingDetails:**
```python
{
  "appointment_type": AppointmentType,
  "date": str,
  "start_time": str,
  "end_time": str,
  "patient": Patient,
  "reason": Optional[str]
}
```

**Patient:**
```python
{
  "name": str,
  "email": EmailStr,  # Validated email format
  "phone": str
}
```

### Data Storage

**doctor_schedule.json Structure:**
```json
{
  "working_hours": {
    "monday": {"start": "09:00", "end": "17:00"},
    "tuesday": {"start": "09:00", "end": "17:00"},
    "wednesday": {"start": "09:00", "end": "17:00"},
    "thursday": {"start": "09:00", "end": "17:00"},
    "friday": {"start": "09:00", "end": "17:00"},
    "saturday": null,
    "sunday": null
  },
  "existing_bookings": [
    {
      "date": "2024-01-15",
      "start_time": "09:30",
      "end_time": "10:00"
    }
  ]
}
```

**RUNTIME_BOOKINGS Structure:**
```python
{
  "2024-01-15": [
    ("10:00", "10:30"),
    ("14:00", "14:30")
  ],
  "2024-01-16": [
    ("11:00", "11:30")
  ]
}
```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_agent.py

# Run with coverage (if pytest-cov installed)
pytest --cov=backend
```

### Test Cases

**1. Health Check Test:**
- Verifies `/health` endpoint returns 200 status
- Checks response contains `{"status": "ok"}`

**2. Availability Test:**
- Tests GET `/api/calendly/availability` endpoint
- Verifies response structure
- Checks that slots are returned

**3. Booking Flow Test:**
- Complete end-to-end booking flow:
  1. Get availability for a date
  2. Find an available slot
  3. Book the slot
  4. Verify booking confirmation
  5. Attempt to book same slot again
  6. Verify conflict error (409 status)

### Test Implementation

Tests use FastAPI's `TestClient` which provides a test interface to the application without running a server. This allows for fast, isolated testing of endpoints.

---

## Additional Notes

### Limitations

1. **No Persistence:** Runtime bookings are stored in-memory and lost on server restart
2. **No Database:** All data is loaded from JSON files
3. **Single Doctor:** System is designed for one doctor's schedule
4. **No Authentication:** No user authentication or authorization
5. **No Email Notifications:** No email sending functionality
6. **No Calendar Integration:** No actual Calendly or calendar system integration

### Future Enhancements

1. Add database persistence (PostgreSQL, SQLite)
2. Implement user authentication
3. Add email notifications
4. Support multiple doctors
5. Add appointment cancellation endpoint
6. Add appointment modification endpoint
7. Implement actual Calendly API integration
8. Add timezone support
9. Add recurring appointment support
10. Add appointment reminders

### Environment Variables

Currently, no environment variables are required. The system is self-contained. If needed in the future, create a `.env` file for:
- Database connection strings
- API keys
- Email service credentials
- Server configuration

### API Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI JSON:** `http://localhost:8000/openapi.json`

These provide:
- All available endpoints
- Request/response schemas
- Try-it-out functionality
- Example requests and responses

---

## Troubleshooting

### Common Issues

1. **Port Already in Use:**
   - Change port: `uvicorn backend.main:app --reload --port 8001`

2. **Module Not Found:**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

3. **Schedule File Not Found:**
   - Verify `data/doctor_schedule.json` exists
   - Check file path in `_load_schedule()` function

4. **Import Errors:**
   - Ensure you're running from project root
   - Check Python path includes project directory

5. **Date Format Errors:**
   - Use YYYY-MM-DD format for dates
   - Use HH:MM format for times (24-hour format)

---

## Conclusion

This documentation provides a comprehensive overview of the Appointment Scheduling Agent project, covering setup, architecture, implementation details, and usage. The system is designed to be simple, self-contained, and easy to understand while demonstrating modern Python web development practices with FastAPI.

For questions or issues, refer to the code comments or the interactive API documentation at `/docs` when the server is running.

