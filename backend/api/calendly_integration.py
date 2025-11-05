import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

from fastapi import APIRouter, HTTPException, Query

from backend.models.schemas import (
    AvailabilityResponse,
    BookingDetails,
    BookingRequest,
    BookingResponse,
    Slot,
)


router = APIRouter()


# Runtime booking only not persisted
RUNTIME_BOOKINGS: Dict[str, List[Tuple[str, str]]] = {}


APPOINTMENT_DURATIONS_MIN = {
    "consultation": 30,
    "followup": 15,
    "physical": 45,
    "special": 60,
}


def _load_schedule() -> Dict:
    data_path = Path(__file__).parents[2] / "data" / "doctor_schedule.json"
    if not data_path.exists():
        raise HTTPException(status_code=500, detail="Schedule data not found")
    with data_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _parse_time(date_str: str, time_str: str) -> datetime:
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")


def _format_time(dt: datetime) -> str:
    return dt.strftime("%H:%M")


def _overlaps(a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime) -> bool:
    return a_start < b_end and b_start < a_end


def _get_weekday(date_str: str) -> str:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"][dt.weekday()]


def _collect_existing_bookings(schedule_data: Dict, date_str: str) -> List[Tuple[datetime, datetime]]:
    # define bookings from file
    file_bookings = []
    for entry in schedule_data.get("existing_bookings", []):
        if entry.get("date") == date_str:
            start = _parse_time(date_str, entry["start_time"])
            end = _parse_time(date_str, entry["end_time"])
            file_bookings.append((start, end))

    # bookings from runtime
    runtime_entries = RUNTIME_BOOKINGS.get(date_str, [])
    for start_str, end_str in runtime_entries:
        start = _parse_time(date_str, start_str)
        end = _parse_time(date_str, end_str)
        file_bookings.append((start, end))
    return file_bookings


def _generate_slots(date_str: str, appointment_type: str) -> List[Slot]:
    schedule_data = _load_schedule()
    weekday = _get_weekday(date_str)
    hours = schedule_data["working_hours"].get(weekday)
    if not hours:
        return []

    duration_min = APPOINTMENT_DURATIONS_MIN[appointment_type]

    day_start = _parse_time(date_str, hours["start"])  
    day_end = _parse_time(date_str, hours["end"]) 

    existing = _collect_existing_bookings(schedule_data, date_str)

    slots: List[Slot] = []
    cursor = day_start
    while cursor + timedelta(minutes=duration_min) <= day_end:
        candidate_start = cursor
        candidate_end = cursor + timedelta(minutes=duration_min)

        has_conflict = any(
            _overlaps(candidate_start, candidate_end, b_start, b_end) for b_start, b_end in existing
        )

        slots.append(
            Slot(
                start_time=_format_time(candidate_start),
                end_time=_format_time(candidate_end),
                available=not has_conflict,
            )
        )

        cursor = cursor + timedelta(minutes=duration_min)

    return slots


@router.get("/availability", response_model=AvailabilityResponse)
def get_availability(date: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"), appointment_type: str = Query(...)):
    if appointment_type not in APPOINTMENT_DURATIONS_MIN:
        raise HTTPException(status_code=400, detail="Invalid appointment_type")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format; expected YYYY-MM-DD")

    slots = _generate_slots(date, appointment_type)
    return AvailabilityResponse(date=date, available_slots=slots)


@router.post("/book", response_model=BookingResponse)
def book_appointment(request: BookingRequest):
    if request.appointment_type not in APPOINTMENT_DURATIONS_MIN:
        raise HTTPException(status_code=400, detail="Invalid appointment_type")

    try:
        start_dt = _parse_time(request.date, request.start_time)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date/time format")

    duration_min = APPOINTMENT_DURATIONS_MIN[request.appointment_type]
    end_dt = start_dt + timedelta(minutes=duration_min)

    available_slots = _generate_slots(request.date, request.appointment_type)
    slot_map = {(s.start_time, s.end_time): s for s in available_slots}
    key = (request.start_time, end_dt.strftime("%H:%M"))
    if key not in slot_map:
        raise HTTPException(status_code=400, detail="Requested time is outside working hours")
    if not slot_map[key].available:
        raise HTTPException(status_code=409, detail="Requested time is no longer available")

    RUNTIME_BOOKINGS.setdefault(request.date, []).append((key[0], key[1]))

    booking_id = f"APPT-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
    confirmation_code = str(uuid.uuid4())[:6].upper()

    details = BookingDetails(
        appointment_type=request.appointment_type,
        date=request.date,
        start_time=request.start_time,
        end_time=key[1],
        patient=request.patient,
        reason=request.reason,
    )

    return BookingResponse(
        booking_id=booking_id,
        status="confirmed",
        confirmation_code=confirmation_code,
        details=details,
    )


