# Log Processing & Alert System

A production-style backend system built with FastAPI that ingests application logs, persists them, and triggers real-time alerts for critical incidents.

## Features
- REST APIs for log ingestion and querying
- Severity-based alert engine
- SQLite persistence using SQLAlchemy
- Email notifications for CRITICAL alerts
- OpenAPI documentation (Swagger)
- Clean modular architecture

## Tech Stack
- Python 3.10
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic v2
- SMTP (Gmail)

## Architecture Flow
1. Client sends logs via POST /logs
2. Logs are validated and persisted
3. CRITICAL logs trigger alert creation
4. Alert emails are sent automatically
5. Alerts can be queried via GET /alerts

## How to Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Visit http://127.0.0.1:8000/docs
