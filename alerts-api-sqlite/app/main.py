from fastapi import FastAPI
from app.init_db import init_db
from app.alerts_router import router as alerts_router
from app.reports_router import router as reports_router
from app.ui_router import router as ui_router

app = FastAPI(
    title="SQLite Alerts API",
    description="Prototype API using SQLite instead of Oracle 19c",
    version="1.0.0"
)

init_db()

app.include_router(alerts_router)
app.include_router(reports_router)
app.include_router(ui_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}