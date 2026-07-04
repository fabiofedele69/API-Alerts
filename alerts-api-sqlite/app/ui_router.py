from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.database import get_connection

router = APIRouter(
    prefix="/ui",
    tags=["User Interface"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def alerts_ui(
    request: Request,
    search: str = "",
    status: str = "",
    alert_type: str = "",
    alert_id: str = "",
    customer_id: str = ""
):
    alerts = []

    if search == "true":
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

        if alert_id:
            sql += " AND alert_id = ?"
            params.append(alert_id)

        if customer_id:
            sql += " AND customer_id = ?"
            params.append(customer_id)

        sql += " ORDER BY created_date DESC"

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        alerts = [dict(row) for row in cursor.fetchall()]
        conn.close()

    return templates.TemplateResponse(
        "alerts.html",
        {
            "request": request,
            "alerts": alerts,
            "search": search,
            "status": status,
            "alert_type": alert_type,
            "alert_id": alert_id,
            "customer_id": customer_id,
            "count": len(alerts)
        }
    )