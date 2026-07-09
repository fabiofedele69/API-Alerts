# API Operations

## Activate the Python Environment

```bash
cd oracle-view-api

source venv/bin/activate
```

---

# Start the API

Execute:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Expected output:

```text
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

The API is now available.

---

# Verify the API

Application status:

```bash
curl http://127.0.0.1:8000/
```

Retrieve all records from the Oracle view in JSON format:

```bash
curl http://127.0.0.1:8000/api/reporter
```

Retrieve the evaluation Excel file:

```bash
curl -o vw_api_reporter.xlsx \
http://127.0.0.1:8000/api/reporter/excel
```

---

# Stop the API

Press:

```text
CTRL + C
```

The Uvicorn server terminates gracefully.

---

# Restart the API

If the server has been stopped:

```bash
source venv/bin/activate

uvicorn app.main:app --host 127.0.0.1 --port 8000
```

---

# Check Whether the API Is Running

```bash
ps -ef | grep uvicorn
```

or

```bash
curl http://127.0.0.1:8000/
```

If the API is running correctly, it returns:

```json
{
  "application": "Oracle Reporter API",
  "status": "running"
}
```

---

# Development Notes

* The API runs locally on `127.0.0.1`.
* The main endpoint `/api/reporter` returns all rows from `LC_SCMT.VW_API_REPORTER` in JSON format.
* The endpoint `/api/reporter/excel` is intended only for evaluation and exports the same data in Microsoft Excel format.
* During this development phase, the API is started manually using Uvicorn. In the deployment phase, it will be managed as a `systemd` service and packaged for automated deployment using Ansible.
