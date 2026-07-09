import oracledb
from app.config import settings


def get_connection():
    dsn = oracledb.makedsn(
        host=settings.ORACLE_HOST,
        port=int(settings.ORACLE_PORT),
        service_name=settings.ORACLE_SERVICE
    )

    connection = oracledb.connect(
        user=settings.ORACLE_USER,
        password=settings.ORACLE_PASSWORD,
        dsn=dsn
    )

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
        cursor.execute(sql)

        columns = [col[0] for col in cursor.description]

        result = []
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))

        return result

    finally:
        cursor.close()
        connection.close()
