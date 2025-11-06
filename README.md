### calendly integration

This project implements the Calendly Integration module as a mock scheduling backend using FastAPI.

It provides two endpoints:
- GET `/api/calendly/availability` — list available time slots for a given date and appointment type
- POST `/api/calendly/book` — confirm a booking for a selected slot

The service simulates:
- Doctor working hours and existing bookings (loaded from `data/doctor_schedule.json`)
- Appointment type durations (15/30/45/60 minutes)
- Conflict detection, no-availability handling, clean JSON responses

### Tech Stack used
- FastAPI (Python 3.10+)
- Uvicorn

### Project Structure
appointment-scheduling-agent/
  README.md
  .env.example
  requirements.txt
  backend/
    main.py
    api/
      calendly_integration.py
    models/
      schemas.py
  data/
    doctor_schedule.json
  tests/
    test_agent.py

### how to setup project
1) Python 3.10+
2) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate
3) Install dependencies
-----pip install -r requirements.txt

4) Copy env file (no secrets required for mock)
-----cp .env.example .env

### How to run 
go to you project folder into the terminal
uvicorn backend.main:app --reload --port 8000

Option B: run from anywhere using --app-dir
uvicorn backend.main:app --reload --port 8000 --app-dir /Users/ldt/Desktop/assignment01/appointment-scheduling-agent

Open docs: `http://localhost:8000/docs`

### Endpoints for APIs
#### GET /api/calendly/availability
Query params:
- `date` (YYYY-MM-DD), e.g., `2024-01-15`
- `appointment_type` in {`consultation`, `followup`, `physical`, `special`}

Response example:
{
  "date": "2024-01-15",
  "available_slots": [
    {"start_time": "09:00", "end_time": "09:30", "available": true},
    {"start_time": "09:30", "end_time": "10:00", "available": false},
    {"start_time": "10:00", "end_time": "10:30", "available": true}
  ]
}

Example curl:
curl "http://localhost:8000/api/calendly/availability?date=2024-01-15&appointment_type=consultation"

#### POST /api/calendly/book
Body example:
{
  "appointment_type": "consultation",
  "date": "2024-01-15",
  "start_time": "10:00",
  "patient": {
    "name": "Akash kumar",
    "email": "akash@example.com",
    "phone": "+1-555-0100"
  },
  "reason": "Annual checkup"
}

Response example:
{
  "booking_id": "APPT-2024-001",
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

Example curl:
curl -X POST http://localhost:8000/api/calendly/book \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_type": "consultation",
    "date": "2024-01-15",
    "start_time": "10:00",
    "patient": {"name": "Akash Kumar", "email": "akash@example.com", "phone": "+1-555-0100"},
    "reason": "Annual checkup"
  }'

### Scheduling Logic
- Appointment durations:
  - consultation: 30 minutes
  - followup: 15 minutes
  - physical: 45 minutes
  - special: 60 minutes
- Working hours come from `data/doctor_schedule.json` by weekday
- Existing bookings come from `data/doctor_schedule.json` by date
- We generate candidate slots across working hours at the selected duration and mark any that overlap with existing bookings as unavailable
- If no slots are available, we return an empty `available_slots` array (you can adapt UI to suggest alternatives)

### Testing
Basic automated tests live in `tests/test_agent.py`. Run with:
pytest -q

### Notes
- This is a self-contained mock; no external Calendly or database is required.
- Data is loaded from JSON at startup; bookings during runtime are kept in-memory and not persisted.


