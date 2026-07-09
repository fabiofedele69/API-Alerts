import oracledb

from app.config import settings
from app.logger import logger


def get_connection():

    logger.info("Opening Oracle connection")

    dsn = oracledb.makedsn(
        settings.ORACLE_HOST,
        int(settings.ORACLE_PORT),
        service_name=settings.ORACLE_SERVICE
    )

    connection = oracledb.connect(
        user=settings.ORACLE_USER,
        password=settings.ORACLE_PASSWORD,
        dsn=dsn
    )

    logger.info("Oracle connection established")

    return connection


def fetch_reporter_data():

    sql = """
    SELECT
        FIELD_01,
        FIELD_02,
        FIELD_03,
        FIELD_04,
        FIELD_05,
        FIELD_06,
        FIELD_07,
        FIELD_08,
        FIELD_09,
        FIELD_10
    FROM LC_SCMT.VW_API_REPORTER
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        logger.info("Executing Oracle query")

        cursor.execute(sql)

        columns = [column[0] for column in cursor.description]

        rows = cursor.fetchall()

        result = [
            dict(zip(columns, row))
            for row in rows
        ]

        logger.info("Returned %s rows", len(result))

        return result

    finally:

        cursor.close()
        connection.close()

        logger.info("Oracle connection closed")
