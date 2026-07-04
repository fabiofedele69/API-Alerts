from app.database import get_connection


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            alert_id TEXT PRIMARY KEY,
            alert_status TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            created_date TEXT NOT NULL,
            customer_id TEXT NOT NULL,
            customer_name TEXT,
            risk_score INTEGER,
            amount REAL,
            currency TEXT,
            country TEXT
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM alerts")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany("""
            INSERT INTO alerts (
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
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            ("A001", "OPEN", "AML", "2026-07-04", "C001", "Customer One", 85, 12500.50, "CHF", "CH"),
            ("A002", "CLOSED", "FRAUD", "2026-07-03", "C002", "Customer Two", 60, 7500.00, "EUR", "IT"),
            ("A003", "IN_REVIEW", "SANCTIONS", "2026-07-02", "C003", "Customer Three", 95, 50000.00, "USD", "AE"),
            ("A004", "OPEN", "AML", "2026-07-01", "C004", "Customer Four", 70, 22000.00, "CHF", "CH"),
            ("A005", "OPEN", "STRUCTURING", "2026-06-30", "C005", "Customer Five", 78, 9800.00, "EUR", "DE")
        ])

    conn.commit()
    conn.close()