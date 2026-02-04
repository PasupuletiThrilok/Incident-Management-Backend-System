from fastapi import FastAPI
from app.api.logs import router as logs_router

app = FastAPI(title="Log Processing & Alert System")

app.include_router(logs_router)

@app.get("/health")
def health_check():
    return {"status": "OK"}
