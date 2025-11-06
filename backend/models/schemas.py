from typing import List, Literal, Optional
from pydantic import BaseModel, Field, EmailStr

AppointmentType = Literal["consultation", "followup", "physical", "special"]
class AvailabilityQuery(BaseModel):
    date: str = Field(..., description="YYYY-MM-DD")
    appointment_type: AppointmentType

class Slot(BaseModel):
    start_time: str
    end_time: str
    available: bool

class AvailabilityResponse(BaseModel):
    date: str
    available_slots: List[Slot]
class Patient(BaseModel):
    name: str
    email: EmailStr
    phone: str
class BookingRequest(BaseModel):
    appointment_type: AppointmentType
    date: str
    start_time: str
    patient: Patient
    reason: Optional[str] = None
class BookingDetails(BaseModel):
    appointment_type: AppointmentType
    date: str
    start_time: str
    end_time: str
    patient: Patient
    reason: Optional[str] = None
class BookingResponse(BaseModel):
    booking_id: str
    status: Literal["confirmed", "failed"]
    confirmation_code: str
    details: BookingDetails


