# EduVMStore

## Project Overview

This project involves the development of an **AppStore** for providing applications on an OpenStack platform.
The goal is to enable instructors to deploy applications that can be used by students
in the context of courses without requiring deep knowledge of OpenStack. 
The focus is on automated configuration and easy management.

### Main Features
- **Automated Deployment**: Simplified deployment process with automated steps for configuring VMs,
user accounts, network settings, etc.
- **Support for Various Applications**: The AppStore can provide pre-configured environments
for different applications.

This project is being implemented as part of the "Project" module at DHBW Mannheim
from August 2024 to May 2025.

## Project DEV Setup and Run
### Local Database
* `python eduvmstorebackend/manage.py makemigrations`
* OR `python3 eduvmstorebackend/manage.py makemigrations`
* `python3 eduvmstorebackend/manage.py migrate`
* OR `python eduvmstorebackend/manage.py migrate`
* Double-click the `db.sqlite3` file
* In the pop-up, click on "Download missing Drivers", wait for the installation to complete, and click "OK"

### Start Backend Server Locally (Development):
* Optional: `export ENABLE_KEYSTONE_AUTH=False`
(is set by default, but needed after using the production environment)
* `python3 eduvmstorebackend/manage.py runserver localhost:8000`
* Access via `localhost:8000`

### Start Backend Server Locally (Production behavior with keystone authentication):
* `export ENABLE_KEYSTONE_AUTH=True`
* `python3 eduvmstorebackend/manage.py runserver localhost:8000`
* Access via `localhost:8000`

### API Access
* Access via `localhost:8000/api/<endpoint>`
* `<endpoint>`: e.g., `<base-url>/app-templates/...`, `<base-url>/users/...`

### Run Tests
* `python eduvmstorebackend/manage.py test`
* OR `python3 eduvmstorebackend/manage.py test`