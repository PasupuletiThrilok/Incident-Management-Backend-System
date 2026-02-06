from app.db.models import TicketStatus

ALLOWED_TRANSITIONS = {
    TicketStatus.OPEN: [TicketStatus.IN_PROGRESS],
    TicketStatus.IN_PROGRESS: [TicketStatus.RESOLVED],
    TicketStatus.RESOLVED: [TicketStatus.CLOSED],
    TicketStatus.CLOSED: []
}

def is_valid_transition(current_status, new_status):
    return new_status in ALLOWED_TRANSITIONS[current_status]
