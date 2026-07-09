from io import BytesIO

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from app.db import fetch_reporter_data

app = FastAPI(
    title="Oracle Reporter API",
    description="Internal API exposing Oracle 19c view LC_SCMT.VW_API_REPORTER",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "application": "Oracle Reporter API",
        "status": "running"
    }


@app.get("/api/reporter")
def get_reporter_data():
    """
    Main endpoint.

    Returns all records from LC_SCMT.VW_API_REPORTER as JSON.
    This is the endpoint intended to be consumed by the external application.
    """
    try:
        data = fetch_reporter_data()
        return data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while reading Oracle view: {str(e)}"
        )


@app.get("/api/reporter/excel")
def get_reporter_excel():
    """
    Evaluation endpoint only.

    Returns all records from LC_SCMT.VW_API_REPORTER as an Excel file.
    This endpoint is intended only for validation/testing purposes.
    """
    try:
        data = fetch_reporter_data()

        df = pd.DataFrame(data)

        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="VW_API_REPORTER")

        output.seek(0)

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=vw_api_reporter.xlsx"
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while creating Excel file: {str(e)}"
        )
