from app.db.models import Alert
from app.core.ticket_engine import create_ticket_from_alert

def trigger_alert(db, log):
    alert = Alert(
        service=log.service,
        message=log.message
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)

    # Auto-create ticket
    create_ticket_from_alert(db, alert)

    return alert
