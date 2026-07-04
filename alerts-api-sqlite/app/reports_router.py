from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.database import get_connection
from datetime import datetime
import pandas as pd
import os

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/alerts/excel")
def export_alerts_excel():
    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT
            alert_id,
            alert_status,
            alert_type,
            created_date,
            customer_id,
            customer_name,
            risk_score,
            amount,
            currency,
            country
        FROM alerts
        ORDER BY created_date DESC
    """, conn)

    conn.close()

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"reports/alerts_report_{timestamp}.xlsx"

    df.to_excel(file_path, index=False)

    return FileResponse(
        file_path,
        filename=f"alerts_report_{timestamp}.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )