from io import BytesIO

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from app.db import fetch_reporter_data
from app.logger import logger

app = FastAPI(
    title="Oracle Reporter API",
    version="1.0"
)


@app.on_event("startup")
def startup():

    logger.info("Reporter API started")


@app.on_event("shutdown")
def shutdown():

    logger.info("Reporter API stopped")


@app.get("/")
def health():

    logger.info("Health endpoint invoked")

    return {
        "application": "Reporter API",
        "status": "running"
    }


@app.get("/api/reporter")
def reporter():

    logger.info("GET /api/reporter")

    try:

        data = fetch_reporter_data()

        return data

    except Exception:

        logger.exception("Error retrieving Oracle data")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


@app.get("/api/reporter/excel")
def reporter_excel():

    logger.info("GET /api/reporter/excel")

    try:

        data = fetch_reporter_data()

        dataframe = pd.DataFrame(data)

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            dataframe.to_excel(
                writer,
                sheet_name="VW_API_REPORTER",
                index=False
            )

        output.seek(0)

        logger.info("Excel successfully generated")

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition":
                "attachment; filename=vw_api_reporter.xlsx"
            }
        )

    except Exception:

        logger.exception("Excel generation failed")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
