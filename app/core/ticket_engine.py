from app.db.models import Ticket, TicketPriority

def create_ticket_from_alert(db, alert):
    ticket = Ticket(
        service=alert.service,
        description=alert.message,
        priority=TicketPriority.CRITICAL
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket
