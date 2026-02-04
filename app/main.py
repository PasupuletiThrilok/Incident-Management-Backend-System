from fastapi import FastAPI

app = FastAPI(title="Log Processing & Alert System")

@app.get("/health")
def health_check():
    return {"status": "OK"}
