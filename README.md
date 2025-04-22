# EduVMStore

## Project Overview

This project involves the development of an **AppStore** for providing applications on an OpenStack platform.
The goal is to enable instructors to deploy applications that can be used by students
in the context of courses without requiring deep knowledge of OpenStack. 
The focus is on automated configuration and easy management.

The frontend repo can be found here: https://github.com/samuelhilpert/eduvmstore-ui

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
* `python3 eduvmstorebackend/manage.py runserver 0.0.0.0:8000`
* Access via `localhost:8000`

### Start Backend Server Locally (Production behavior with keystone authentication):
* `python3 eduvmstorebackend/manage.py runserver 0.0.0.0:8000`
* Access via `localhost:8000`

### API Access
* Access via `localhost:8000/api/<endpoint>`
* `<endpoint>`: e.g., `<base-url>/app-templates/...`, `<base-url>/users/...`

### Run Tests
* `python eduvmstorebackend/manage.py test`
* OR `python3 eduvmstorebackend/manage.py test`

### Use Cloud-Init-Script for faster Setup
* On `https://stack.dhbw.cloud/` create new instance
* At Source choose Image as Boot Source, Ubuntu 22.04 as Image and no new Volume
* Choose your Flavor of choice
* For Network choose provider_912
* The Security Group should allow ingress TCP connections on port 8000 and 22
* Choose your SSH Keypair of choice to access the VM through ssh
* At Configuration upload the Cloud-Init-Script backendscript.yaml
* Launch the Instance
* Access the Instance using `ssh ubuntu@<instance-ip> -i <path-to-keyfile>`
* Execute `/initilization_script`
* To manage the Backend-Service you can use:
* `sudo systemctl enable eduvmstorebackend`
* `sudo systemctl start eduvmstorebackend`
* `sudo systemctl stop eduvmstorebackend`
* `sudo systemctl restart eduvmstorebackend`
