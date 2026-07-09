# Oracle Reporter API

## Overview

Oracle Reporter API is a Python REST service that exposes the Oracle 19c view `LC_SCMT.VW_API_REPORTER`.

The application is built using FastAPI and Uvicorn and initially runs only on `localhost`. Its primary purpose is to provide all records from the Oracle view in JSON format to an internal consumer application. A secondary endpoint is available to export the same data as an Excel file for evaluation and testing.

## Features

* Oracle Database 19c connectivity
* FastAPI REST service
* Uvicorn application server
* GET endpoints
* JSON output
* Excel export for evaluation
* Configuration through environment variables
* Centralized logging
* Read-only Oracle access

## Project Structure

```text
oracle-view-api/
│
├── app/
│   ├── main.py
│   ├── db.py
│   ├── config.py
│   └── logger.py
│
├── logs/
├── .env
├── requirements.txt
└── README.md
```

## Installation

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure Oracle credentials in the `.env` file.

## Start the API

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Endpoints

### Health Check

```
GET /
```

### JSON Output

```
GET /api/reporter
```

Returns all rows from `LC_SCMT.VW_API_REPORTER` in JSON format.

### Excel Output

```
GET /api/reporter/excel
```

Returns an Excel workbook containing all rows from the Oracle view. This endpoint is intended for evaluation and testing.

## Logging

Application logs are written to:

```text
logs/reporter_api.log
```

The application logs:

* Startup and shutdown
* Incoming API requests
* Oracle connection events
* Query execution
* Number of returned rows
* Excel generation
* Errors and exceptions

## Security

Current version:

* Localhost only (`127.0.0.1`)
* Read-only Oracle account
* Configuration through environment variables

Future versions will include HTTPS, authentication, packaging as an RPM, `systemd` integration, and deployment through Ansible.
