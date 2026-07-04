# Oracle 19c Integration Checklist

## Objective

Integrate the current FastAPI prototype with the Oracle 19c database used by the application, replacing the SQLite backend while keeping the REST API, Business UI and report generation unchanged.

---

# 1. Development Environment

## Verify Python installation

- [ ] Verify Python version

```bash
python --version
```

Expected:
- Python 3.9 or newer

---

## Verify pip

```bash
pip --version
```

---

## Create Virtual Environment (if Anaconda is not available)

Linux / RHEL / DevPod

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

---

## Install required packages

```bash
pip install -r requirements.txt
```

Verify installation

```bash
pip list
```

Expected packages

- fastapi
- uvicorn
- pandas
- openpyxl
- jinja2
- python-dotenv
- oracledb

---

# 2. Oracle Environment

Collect the following information.

## Oracle Host

- [ ] Oracle server hostname

Example

```
oracle-server.company.com
```

---

## Oracle Port

Usually

```
1521
```

---

## Oracle Service Name

Example

```
ORCLPDB
```

or

```
CMDB
```

---

## Oracle SID (if used)

Only if applicable.

---

## Oracle Schema

Expected

```
LC_SCMT
```

---

## Oracle Read-Only User

Verify that a dedicated API user exists.

Example

```
API_READ_USER
```

The user should have ONLY

- CREATE SESSION
- SELECT

No INSERT

No UPDATE

No DELETE

---

## Required Grants

Example

```sql
GRANT CREATE SESSION TO API_READ_USER;

GRANT SELECT ON LC_SCMT.ALERTS TO API_READ_USER;
```

---

# 3. Network Connectivity

Verify that the DevPod can reach Oracle.

Example

```bash
nc -vz oracle-server.company.com 1521
```

or

```bash
telnet oracle-server.company.com 1521
```

Questions

- [ ] Is the Oracle port reachable?
- [ ] Firewall open?
- [ ] VPN required?

---

# 4. Oracle Client

Determine whether the environment requires

## Thin Mode

Preferred

No Oracle Client required.

---

## Thick Mode

Ask

- [ ] Is Oracle Instant Client required?
- [ ] Oracle Wallet?
- [ ] tnsnames.ora?
- [ ] LDAP?
- [ ] TCPS?

---

# 5. Oracle Connection Test

Before modifying the API, create a simple script.

Example

```python
from app.database import get_connection

conn = get_connection()

cursor = conn.cursor()

cursor.execute("SELECT 1 FROM dual")

print(cursor.fetchone())

cursor.close()
conn.close()
```

Expected

```
(1,)
```

---

# 6. Database Discovery

Confirm schema

```
LC_SCMT
```

---

## Discover tables

Example

```sql
SELECT table_name
FROM all_tables
WHERE owner='LC_SCMT';
```

---

## Discover columns

Example

```sql
SELECT column_name,
       data_type
FROM all_tab_columns
WHERE owner='LC_SCMT'
AND table_name='ALERTS'
ORDER BY column_id;
```

---

## Verify

- [ ] Primary Key
- [ ] Foreign Keys
- [ ] Indexes
- [ ] Views
- [ ] Materialized Views

---

# 7. Business Requirements

Identify the first report.

Questions

- Which table?
- Which columns?
- Which filters?
- Sorting?
- Maximum rows?
- Excel?
- CSV?
- PDF?

---

## Expected Filters

Examples

- Alert ID
- Customer ID
- Alert Status
- Alert Type
- Created Date From
- Created Date To
- Owner
- Priority

---

# 8. SQL Queries

Collect the real SQL.

Example

```sql
SELECT
    ALERT_ID,
    ALERT_STATUS,
    ALERT_TYPE
FROM LC_SCMT.ALERTS;
```

Understand

- joins
- views
- performance
- indexes

---

# 9. Reports

Identify all reports.

Example

- Alerts Report
- Open Alerts
- Closed Alerts
- High Risk Alerts
- Alerts by Customer
- Alerts by Date
- Alerts by Owner

For each report identify

- SQL
- Filters
- Excel output
- Sheet name

---

# 10. Application Security

Questions

- [ ] Who can invoke the API?
- [ ] Internal users only?
- [ ] JWT?
- [ ] OAuth2?
- [ ] Corporate SSO?
- [ ] API Key?

---

# 11. Logging

Verify

- Log location
- Log rotation
- Error logging
- Audit requirements

---

# 12. Deployment

Determine

- DevPod OS
- Python version
- RHEL version
- Reverse Proxy (Nginx?)
- systemd service?
- HTTPS?

---

# 13. Performance

Questions

- Expected number of alerts
- Average report size
- Maximum report size
- Query execution time
- Pagination required?

---

# 14. Future Improvements

Possible enhancements

- Authentication
- Authorization
- Multiple reports
- Report Scheduler
- Email reports
- PDF reports
- Dashboard
- Charts
- Report history
- Audit log
- Role-based access
- Oracle Views
- REST versioning
- Unit Tests
- Docker deployment

---

# 15. End of Day Goal

By the end of the Oracle integration session the application should:

- [ ] Connect successfully to Oracle 19c
- [ ] Use the real LC_SCMT schema
- [ ] Execute the first production SQL query
- [ ] Display Oracle data in the Business UI
- [ ] Expose Oracle data through the REST API
- [ ] Generate the first Excel report from Oracle
- [ ] Keep the same FastAPI architecture
- [ ] Keep the SQLite backend available for local development
