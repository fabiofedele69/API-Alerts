# API Reporter

## Overview

API Reporter is a Python-based REST API used to retrieve reporting information from the Oracle 19c database for the SCMT platform.

The application is packaged as an RPM and deployed on RHEL servers using the UBS CI/CD pipeline.

Deployment flow:

```
GitLab
    │
    ▼
Pipeline
    │
    ▼
RPM Build
    │
    ▼
Nexus Repository
    │
    ▼
Ansible
    │
    ▼
REX Deployment
    │
    ▼
Target RHEL Servers
```

---

# Architecture

```
                 +----------------------+
                 |     REST Client      |
                 +----------+-----------+
                            |
                            |
                     HTTP / HTTPS
                            |
                            ▼
                  Apache HTTP Server
                     (httpd)
                            |
                   Reverse Proxy
                            |
                            ▼
                  API Reporter Service
                  (systemd service)
                            |
                            ▼
                    FastAPI Application
                            |
                            ▼
                    Oracle 19c Database
```

The API Reporter runs as a systemd service.

Apache HTTP Server exposes the REST endpoints and forwards incoming requests to the FastAPI application.

---

# Installation

Deployment is fully automated.

The deployment sequence is:

1. Build RPM
2. Publish RPM to Nexus
3. Update Ansible version
4. Execute REX deployment
5. RPM installation
6. Service startup

No manual installation is normally required.

---

# RPM Lifecycle

The RPM contains four scriptlets.

## Pre-install

Executed before installing the package.

Responsibilities:

- Validate application user
- Validate application group
- Validate Python installation
- Stop the running service during upgrades

---

## Post-install

Executed after package installation.

Responsibilities:

- Create runtime directories
- Create Python virtual environment (if necessary)
- Install Python dependencies
- Install systemd service
- Set permissions
- Reload systemd
- Enable the service
- Restart the service
- Verify that the service is active

---

## Pre-remove

Executed before package removal.

Behavior:

### Package removal

```
systemctl stop api-reporter
systemctl disable api-reporter
```

### Package upgrade

During an upgrade the script detects the RPM transaction and **does not stop** the service.

This prevents the service from being stopped after the new version has already been restarted.

---

## Post-remove

Reloads the systemd daemon.

---

# Operational Commands

## Verify installed version

```bash
rpm -q m50-api-reporter
```

Example:

```
m50-api-reporter-2.34.0.2-8.el7.ubs.noarch
```

---

## Check service status

```bash
systemctl status api-reporter
```

---

## Verify service is active

```bash
systemctl is-active api-reporter
```

Expected:

```
active
```

---

## Verify service is enabled

```bash
systemctl is-enabled api-reporter
```

Expected:

```
enabled
```

---

## Start service

```bash
systemctl start api-reporter
```

---

## Stop service

```bash
systemctl stop api-reporter
```

---

## Restart service

```bash
systemctl restart api-reporter
```

---

## View logs

```bash
journalctl -u api-reporter
```

Live monitoring:

```bash
journalctl -fu api-reporter
```

---

# Deployment Procedure

## New Version

1. Update project version.
2. Commit changes.
3. Push to GitLab.
4. Create RPM tag.
5. Wait for pipeline completion.
6. Verify RPM publication in Nexus.
7. Update Ansible inventory version.
8. Commit Ansible changes.
9. Create Ansible tag.
10. Execute deployment using REX.
11. Verify service status.

---

# Validation Checklist

After every deployment verify:

```bash
rpm -q m50-api-reporter

systemctl is-active api-reporter

systemctl is-enabled api-reporter

systemctl status api-reporter
```

Expected:

- Correct RPM version installed
- Service active
- Service enabled
- No startup errors

---

# Upgrade Validation

The following scenarios have been validated.

## Fresh Installation

```
No RPM installed
        │
        ▼
Install RPM
        │
        ▼
Service starts correctly
```

Result:

PASS

---

## Upgrade

```
Version 2.34.0.1
        │
        ▼
Upgrade
        │
        ▼
Version 2.34.0.2
        │
        ▼
Service remains active
```

Result:

PASS

---

## Reinstallation

```
Remove RPM
        │
        ▼
Deploy same version
        │
        ▼
Fresh installation completed
```

Result:

PASS

---

# Troubleshooting

## Check RPM version

```bash
rpm -q m50-api-reporter
```

---

## Check service logs

```bash
journalctl -u api-reporter
```

---

## Check Apache configuration

```bash
find / -name httpd.conf 2>/dev/null
```

Typical location:

```
/etc/httpd/conf/httpd.conf
```

---

## Verify Apache service

```bash
systemctl status httpd
```

---

## Verify Python environment

```bash
python3 --version
```

---

## Verify API process

```bash
ps -ef | grep api-reporter
```

---

# Support

When reporting an issue always collect:

- RPM version
- Service status
- Journal logs
- Apache status
- Deployment version
- REX execution logs
- Pipeline ID
