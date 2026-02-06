# Incident Management Backend System

A production-style backend system designed to ingest application logs, detect critical incidents, and automatically create and manage incident tickets with workflow and SLA tracking.

This project simulates how real-world IT services and platform teams monitor systems, respond to incidents, and track resolution status.


## Problem Statement

Modern applications generate large volumes of logs, but critical failures require structured tracking and resolution rather than manual monitoring.

This system addresses that gap by:
- Ingesting logs through APIs
- Detecting critical incidents
- Automatically creating incident tickets
- Managing ticket lifecycle with controlled workflows
- Tracking SLA metrics for incident resolution


## System Overview

The system follows an event-driven flow:
Logs → Alerts → Tickets → Resolution Tracking


1. Applications send logs to the system  
2. CRITICAL logs trigger alerts  
3. Alerts automatically create incident tickets  
4. Tickets follow a controlled lifecycle  
5. Resolution timestamps enable SLA analysis  

Notification channels (email, Slack, etc.) are intentionally decoupled from core logic to ensure system reliability even if external services fail.


## Key Features

- REST APIs for log ingestion and querying
- Automatic alert generation for CRITICAL logs
- Auto-creation of incident tickets from alerts
- Ticket lifecycle management (OPEN → IN_PROGRESS → RESOLVED → CLOSED)
- Priority handling for incidents
- SLA tracking using resolution timestamps
- Filtering and querying tickets by status and priority
- Clean, modular backend architecture


## Architecture

Client<br>
↓<br>
Logs API (FastAPI)<br>
↓<br>
Alert Engine<br>
↓<br>
Ticket Engine<br>
↓<br>
Ticket Management APIs<br>


Each layer is decoupled to allow easy extension and maintenance.

## Tech Stack

- Python 3.10
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- REST APIs


## API Overview

### Logs
- `POST /logs` – Ingest application logs
- `GET /logs` – Query stored logs

### Alerts
- `GET /alerts` – View generated alerts

### Tickets
- `GET /tickets` – List all tickets
- `GET /tickets/{id}` – View ticket details
- `PATCH /tickets/{id}` – Update ticket status
- `PATCH /tickets/{id}/priority` – Update ticket priority


## SLA Tracking

The system tracks incident resolution time by recording timestamps when tickets transition to the `RESOLVED` state.

This enables:
- Measuring response efficiency
- Identifying long-running incidents
- Supporting future SLA reporting and analytics


## How to Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Access API documentation:
http://127.0.0.1:8000/docs


## Note: Why This Project
This project was built to simulate real-world incident management systems used by IT services and platform teams.
It focuses on backend design, workflow enforcement, and reliability, rather than UI or superficial features.

## Caution
This project is intended for learning and demonstration purposes only.
