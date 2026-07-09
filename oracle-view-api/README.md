# Environment Setup

## Purpose

The Oracle Reporter API exposes the Oracle 19c view `LC_SCMT.VW_API_REPORTER` through a REST API implemented in Python using FastAPI.

The API is intended to run locally on the application server (`localhost`) and will be consumed by an internal application.

---

# Target Environment

| Component            | Requirement                             |
| -------------------- | --------------------------------------- |
| Operating System     | Red Hat Enterprise Linux 7 or 8         |
| Database             | Oracle Database 19c                     |
| Programming Language | Python 3.10 or later                    |
| Web Framework        | FastAPI                                 |
| Application Server   | Uvicorn                                 |
| Oracle Driver        | python-oracledb (Thin Mode recommended) |

---

# Required Software

Verify that the following software is installed.

## Python

```bash
python3 --version
```

Expected output:

```text
Python 3.10.x
```

---

## pip

```bash
pip3 --version
```

---

## Python Virtual Environment

```bash
python3 -m venv --help
```

---

# Create the Virtual Environment

```bash
python3 -m venv venv
```

Activate it

```bash
source venv/bin/activate
```

---

# Install Required Python Packages

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains:

```text
fastapi
uvicorn
oracledb
python-dotenv
pandas
openpyxl
```

---

# Oracle Configuration

Create a `.env` file containing the Oracle connection parameters.

Example:

```text
ORACLE_USER=scmt_api
ORACLE_PASSWORD=********
ORACLE_HOST=myoracle.company.com
ORACLE_PORT=1521
ORACLE_SERVICE=ORCLPDB
```

---

# Oracle Permissions

The Oracle user requires only the following privileges:

* CREATE SESSION
* SELECT on `LC_SCMT.VW_API_REPORTER`

No INSERT, UPDATE or DELETE permissions are required.

---

# Network Configuration

During the first development phase, the API listens only on:

```text
127.0.0.1:8000
```

No external access is allowed.

HTTPS, authentication and reverse proxy configuration will be introduced during the deployment phase.

---

# Project Structure

```text
oracle-view-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── db.py
│   └── config.py
│
├── requirements.txt
├── .env
└── README.md
```
