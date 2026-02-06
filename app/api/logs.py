from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import Literal, List
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import Alert, Log
from app.core.alert_engine import trigger_alert
from typing import List, Optional
from app.db.models import Ticket, TicketStatus, TicketPriority
from app.core.ticket_workflow import is_valid_transition
from fastapi import HTTPException



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

class AlertResponse(BaseModel):
    service: str
    message: str
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/logs", response_model=LogResponse)
def ingest_log(log: LogRequest, db: Session = Depends(get_db)):
    db_log = Log(
        service=log.service,
        level=log.level,
        message=log.message
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    if log.level == "CRITICAL":
        trigger_alert(db, db_log)

    return db_log

@router.get("/logs", response_model=List[LogResponse])
def get_logs(level: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Log)

    if level:
        query = query.filter(Log.level == level)

    return query.order_by(Log.timestamp.desc()).all()

@router.get("/alerts", response_model=List[AlertResponse])
def get_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).order_by(Alert.timestamp.desc()).all()

class TicketResponse(BaseModel):
    id: int
    service: str
    description: str
    priority: TicketPriority
    status: TicketStatus
    created_at: datetime
    resolved_at: datetime | None

    model_config = {
        "from_attributes": True
    }

'''@router.get("/tickets", response_model=list[TicketResponse])
def get_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).order_by(Ticket.created_at.desc()).all()'''

class TicketStatusUpdate(BaseModel):
    status: TicketStatus

@router.patch("/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket_status(
    ticket_id: int,
    payload: TicketStatusUpdate,
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if not is_valid_transition(ticket.status, payload.status):
        raise HTTPException(
            status_code=400,
            detail="Invalid status transition from"
        )

    ticket.status = payload.status

    if payload.status == TicketStatus.RESOLVED:
        ticket.resolved_at = datetime.utcnow()

    db.commit()
    db.refresh(ticket)

    return ticket

'''@router.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket_by_id(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket'''

class TicketPriorityUpdate(BaseModel):
    priority: TicketPriority

@router.patch("/tickets/{ticket_id}/priority", response_model=TicketResponse)
def update_ticket_priority(
    ticket_id: int,
    payload: TicketPriorityUpdate,
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.priority = payload.priority
    db.commit()
    db.refresh(ticket)

    return ticket

@router.get("/tickets", response_model=list[TicketResponse])
def get_tickets(
    status: Optional[TicketStatus] = None,
    priority: Optional[TicketPriority] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Ticket)

    if status is not None:
        query = query.filter(Ticket.status == status)

    if priority is not None:
        query = query.filter(Ticket.priority == priority)

    return query.order_by(Ticket.created_at.desc()).all()