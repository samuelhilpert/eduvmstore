# EduVMStore Backend

## Overview

EduVMStore is a backend service designed to power an AppStore for deploying applications on an OpenStack platform. It allows instructors to easily provide pre-configured applications to students, facilitating a smoother educational experience without requiring deep technical knowledge of OpenStack.

This project is developed as part of the "Projektkonzeption und -realisierung" module at DHBW Mannheim (August 2024 - May 2025).

Frontend repository: [eduvmstore-ui](https://github.com/samuelhilpert/eduvmstore-ui)

---

## Key Features

* **Automated Deployment**: Handles virtual machine setup, user configuration, and network management.
* **Multi-Application Support**: Provides pre-configured environments for various educational tools.
* **Streamlined Management**: Offers simple interfaces for managing deployments and resources.

---

## Getting Started

### Prerequisites

* Python 3.12
* `pip` package manager
* OpenStack environment (for deployment)

### Environment Configuration

To manage development and testing configurations, create a `.env` file in the `eduvmstorebackend/config` directory. Populate it with the following variables:

```dotenv
# env
SECRET_KEY=<your-secret-key>
DEBUG=<True-or-False>
ALLOWED_HOSTS=<your-allowed-hosts-separated-by-comma>
CORS_ALLOW_ALL_ORIGINS=<True-or-False>
OPENSTACK_AUTH_URL=<your-openstack-auth-url>
SQLITE_DB_NAME=<your-sqlite-db-name>
```

For production deployments, set these variables using system environment tools like `export` or service managers such as systemd or Docker.

---

## Database Setup

Run the following commands to initialize the database schema:

```bash
python3 eduvmstorebackend/manage.py makemigrations
python3 eduvmstorebackend/manage.py migrate
```

---

## Running the Server

Start the backend development server using:

```bash
python3 eduvmstorebackend/manage.py runserver 0.0.0.0:8000
```

Access the server at: `http://localhost:8000`

---

## API Usage

Base URL: `http://localhost:8000/api/`

Example endpoints:

* `app-templates/`
* `users/`

---

## Running Tests

Execute the test suite to validate your setup:

```bash
python3 eduvmstorebackend/manage.py test
```

---

## Deployment on OpenStack

### Quick Setup with Cloud-Init Script

1. Go to [stack.dhbw.cloud](https://stack.dhbw.cloud/) and create a new instance.

2. Instance Configuration:

   * Image: Ubuntu 22.04
   * Flavor: Select according to your resource needs
   * Network: Use `provider_912`
   * Security Group: Allow TCP on ports 8000 and 22
   * SSH Keypair: Use your public SSH key

3. Upload `backendscript.yaml` in the configuration section.

4. Launch and connect via SSH:

   ```bash
   ssh ubuntu@<instance-ip> -i <path-to-keyfile>
   ```

5. Execute the initialization script:

   ```bash
   /initialization_script
   ```

---

### Managing the Backend Service

Control the backend service using systemd:

```bash
sudo systemctl enable eduvmstorebackend
sudo systemctl start eduvmstorebackend
sudo systemctl stop eduvmstorebackend
sudo systemctl restart eduvmstorebackend
```

---

## License

This project is licensed under the MIT License. For full details, see the [LICENSE](./LICENSE) file.
