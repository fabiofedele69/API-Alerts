# Operations Guide

## Start the API

Move to the project directory:

```bash
cd /home/oracle-view-api
```

Activate the Python virtual environment:

```bash
source venv/bin/activate
```

Start the API:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The console should display:

```text
INFO:     Started server process
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

The API is now available.

---

## Verify the API

Health check:

```bash
curl http://127.0.0.1:8000/
```

Retrieve all data as JSON:

```bash
curl http://127.0.0.1:8000/api/reporter
```

Download the evaluation Excel file:

```bash
curl -o vw_api_reporter.xlsx \
http://127.0.0.1:8000/api/reporter/excel
```

---

## Monitor the Logs

Display the application log in real time:

```bash
tail -f logs/reporter_api.log
```

Search for errors:

```bash
grep ERROR logs/reporter_api.log
```

---

## Stop the API

If the API is running in the foreground, press:

```text
CTRL + C
```

The application stops gracefully.

---

## Restart the API

Restart by executing:

```bash
source venv/bin/activate

uvicorn app.main:app --host 127.0.0.1 --port 8000
```

---

## Verify that the Process Is Running

```bash
ps -ef | grep uvicorn
```

or

```bash
curl http://127.0.0.1:8000/
```

---

# External Application Integration

The external application consumes the API by sending an HTTP GET request.

JSON endpoint:

```
GET http://127.0.0.1:8000/api/reporter
```

The API returns all rows from the Oracle view in JSON format.

Example response:

```json
[
  {
    "FIELD_01": "ABC",
    "FIELD_02": "123",
    "FIELD_03": "XYZ"
  },
  {
    "FIELD_01": "DEF",
    "FIELD_02": "456",
    "FIELD_03": "UVW"
  }
]
```

The external application only needs to:

1. Open an HTTP connection.
2. Execute an HTTP GET request.
3. Read the JSON response.
4. Parse the JSON according to its own implementation.

The API is completely stateless. Every GET request executes a new query against the Oracle view and returns the current contents of `LC_SCMT.VW_API_REPORTER`.

During the development phase, the API is reachable only from the local server (`127.0.0.1`).

During the deployment phase, the API will be exposed through the enterprise web infrastructure (for example Nginx or Apache) and accessed using a corporate URL such as:

```
https://api.company.com/reporter/api/reporter
```

No changes will be required in the application logic; only the endpoint URL will change.
