from fastapi import FastAPI
from backend.api.calendly_integration import router as calendly_router


app = FastAPI(title="Medical Appointment Scheduling Agent — Calendly Mock")


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(calendly_router, prefix="/api/calendly", tags=["calendly"])


