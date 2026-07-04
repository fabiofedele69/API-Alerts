from fastapi import APIRouter, Query # type: ignore
from typing import Optional
from app.database import get_connection # type: ignore

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get("/")
def get_alerts(
    limit: int = Query(default=100, ge=1, le=1000),
    status: Optional[str] = None,
    alert_type: Optional[str] = None
):
    sql = """
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
        WHERE 1 = 1
    """

    params = []

    if status:
        sql += " AND alert_status = ?"
        params.append(status)

    if alert_type:
        sql += " AND alert_type = ?"
        params.append(alert_type)

    sql += " ORDER BY created_date DESC LIMIT ?"
    params.append(limit)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


@router.get("/{alert_id}")
def get_alert_by_id(alert_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
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
        WHERE alert_id = ?
    """, (alert_id,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {"message": "Alert not found"}

    return dict(row)
