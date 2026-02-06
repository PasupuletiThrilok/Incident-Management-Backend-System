from fastapi import FastAPI
from app.api.logs import router as logs_router
from app.db.database import engine
from app.db import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Log Processing & Alert System")

app.include_router(logs_router)

@app.get("/health")
def health_check():
    return {"status": "OK"}
