from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Literal

router = APIRouter()

class LogRequest(BaseModel):
    service: str
    level: Literal["INFO", "WARNING", "ERROR", "CRITICAL"]
    message: str

class LogResponse(BaseModel):
    service: str
    level: str
    message: str
    timestamp: datetime
@router.post("/logs", response_model=LogResponse)
def ingest_log(log: LogRequest):
    log_entry = {
        "service": log.service,
        "level": log.level,
        "message": log.message,
        "timestamp": datetime.utcnow()
    }

    # For now, just print (DB comes next)
    print(f"[{log_entry['level']}] {log_entry['service']}: {log_entry['message']}")

    return log_entry
