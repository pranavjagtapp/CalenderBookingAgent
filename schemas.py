from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserMessage(BaseModel):
    message: str

class Node(BaseModel):
    # example structure
    id: int
    name: str
    timestamp: str    

class BookingRequest(BaseModel):
    date: str  # e.g. "2025-07-01"
    time: str  # e.g. "15:30"
    duration_minutes: Optional[int] = 30
    summary: Optional[str] = "Meeting"

class BookingResponse(BaseModel):
    success: bool
    message: str
    event_link: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
