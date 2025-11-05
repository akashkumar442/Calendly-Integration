from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_availability_ok():
    r = client.get("/api/calendly/availability", params={"date": "2024-01-15", "appointment_type": "consultation"})
    assert r.status_code == 200
    body = r.json()
    assert body["date"] == "2024-01-15"
    assert isinstance(body["available_slots"], list)


def test_booking_flow():
    # Find a first available consultation slot on 2024-01-15
    avail = client.get("/api/calendly/availability", params={"date": "2024-01-15", "appointment_type": "consultation"}).json()
    available_slot = next((s for s in avail["available_slots"] if s["available"]), None)
    assert available_slot is not None

    payload = {
        "appointment_type": "consultation",
        "date": "2024-01-15",
        "start_time": available_slot["start_time"],
        "patient": {"name": "John Doe", "email": "john@example.com", "phone": "+1-555-0100"},
        "reason": "Annual checkup"
    }

    r = client.post("/api/calendly/book", json=payload)
    assert r.status_code == 200
    booked = r.json()
    assert booked["status"] == "confirmed"
    assert booked["details"]["start_time"] == payload["start_time"]

    # Try to book the same slot again; should conflict
    r2 = client.post("/api/calendly/book", json=payload)
    assert r2.status_code == 409


