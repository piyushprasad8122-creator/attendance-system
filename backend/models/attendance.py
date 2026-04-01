from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AttendanceRecord(BaseModel):
    user_id: str
    date: str                        # YYYY-MM-DD
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    status: str = "present"          # present, absent, late
    verified_by_face: bool = False

class LeaveRequest(BaseModel):
    reason: str
    from_date: str
    to_date: str
