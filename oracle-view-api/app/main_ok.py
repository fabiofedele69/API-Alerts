from datetime import date, datetime
from decimal import Decimal
from io import BytesIO
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from openpyxl import Workbook

from app.db import fetch_reporter_data
from app.logger import logger


app = FastAPI(
    title="FCSCMT API Reporter",
    description="Internal API exposing the Oracle view VW_API_REPORTER",
    version="1.0.0",
)


@app.on_event("startup")
def startup_event() -> None:
    logger.info("Reporter API started")


@app.on_event("shutdown")
def shutdown_event() -> None:
    logger.info("Reporter API stopped")


@app.get("/")
def health_check():
    """
    Health-check endpoint.

    This endpoint verifies that the API is running.
    It does not execute an Oracle query.
    """
    logger.info("GET / health check")

    return {
        "application": "FCSCMT API Reporter",
        "status": "running",
    }


@app.get("/api/reporter")
def reporter():
    """
    Returns all entries from VW_API_REPORTER as JSON.
    """
    logger.info("GET /api/reporter")

    try:
        data = fetch_reporter_data()

        logger.info(
            "JSON response successfully generated; rows=%s",
            len(data),
        )

        return data

    except Exception:
        logger.exception("Error retrieving Oracle data")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )


def excel_safe_value(value: Any) -> Any:
    """
    Converts Oracle/Python values into values supported by openpyxl.
    """
    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, datetime):
        # Excel does not support timezone-aware datetime objects.
        if value.tzinfo is not None:
            return value.isoformat()

        return value

    if isinstance(value, date):
        return value

    if isinstance(value, bytes):
        return value.hex()

    # Oracle CLOB/BLOB values can expose a read() method.
    if hasattr(value, "read"):
        content = value.read()

        if isinstance(content, bytes):
            return content.hex()

        return str(content)

    return str(value)


@app.get("/api/reporter/excel")
def reporter_excel():
    """
    Returns all entries from VW_API_REPORTER as an Excel file.

    This endpoint is intended for evaluation and validation.
    """
    logger.info("GET /api/reporter/excel")

    try:
        data = fetch_reporter_data()

        workbook = Workbook(write_only=True)
        worksheet = workbook.create_sheet(
            title="VW_API_REPORTER",
        )

        if data:
            columns = list(data[0].keys())

            # Excel header row
            worksheet.append(columns)

            # Excel data rows
            for record in data:
                worksheet.append(
                    [
                        excel_safe_value(record.get(column))
                        for column in columns
                    ]
                )

        output = BytesIO()
        workbook.save(output)
        output.seek(0)

        logger.info(
            "Excel successfully generated; rows=%s",
            len(data),
        )

        return StreamingResponse(
            output,
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            headers={
                "Content-Disposition": (
                    'attachment; filename="vw_api_reporter.xlsx"'
                )
            },
        )

    except Exception:
        logger.exception("Excel generation failed")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )
