# Backend Development Setup

This guide provides step-by-step instructions to set up and run the EduVMStore backend locally or in a
production environment. Choose manual setup for development or use the automated cloud-init script for
production deployment.

---

## Environment Configuration

To manage environment-specific settings (e.g., secrets, debug mode), create a `.env` file in the following
location for **development**:

```
eduvmstorebackend/config/.env
```

Recommended content (replace placeholders with actual values and configure as needed):

```dotenv
SECRET_KEY=<your-secret-key>
DEBUG=<True-or-False>
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,<your-backend-host-ip>
CORS_ALLOW_ALL_ORIGINS=<True-or-False>
OPENSTACK_AUTH_URL=<your-openstack-auth-url (e.g., 1.1.1.1/identity/)>
SQLITE_DB_NAME=db.sqlite3
```

These variables are loaded using `python-decouple`.

> **For production deployments**, set these variables using system environment tools like `export`, or
> configure them via service managers such as `systemd` or Docker.

---

## 1. Manual Setup (Recommended for Development)

### Prerequisites

Ensure the following tools and components are available on your system:

* Python 3.12
* `pip` package manager

### 1.1 Clone the Repository

Navigate to the folder where you want to store the project and clone the repository:

```bash
git clone https://github.com/samuelhilpert/eduvmstore.git
```

```bash
cd eduvmstore
```

### 1.2 Create a Virtual Environment

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install -r eduvmstorebackend/requirements.txt
```

### 1.3 Apply Database Migrations

```bash
python3 eduvmstorebackend/manage.py makemigrations
```

```bash
python3 eduvmstorebackend/manage.py migrate
```

> Tip: After the first migration, you can open `db.sqlite3` using your SQLite viewer. If prompted, allow
> missing drivers to install.

### 1.4 Run the Development Server

```bash
python3 eduvmstorebackend/manage.py runserver 0.0.0.0:8000
```

Access the backend via:

* Local: `http://localhost:8000`
* VM: `http://<vm-ip>:8000`

---

### 1.5 API Access

All API endpoints are exposed under:

`http://<host>:8000/api/`

Example endpoints:

* `/api/app-templates/`
* `/api/users/`

### 1.6 API Testing with Bruno

1. Download: [Bruno Desktop](https://www.usebruno.com/)
2. Open the folder: [`APICollectionEduVMStore`](/APICollectionEduVMStore) with Bruno
3. Configure environments (IP, BASE\_URL, OpenStack credentials)
4. Send the authentication request (sets token for other endpoints)
5. Use other endpoints interactively

---

### 1.7 Run Tests

Execute unit tests to validate the codebase:

```bash
python3 eduvmstorebackend/manage.py test
```

---

## 2. Production Setup Using Cloud-Init Script

This approach automates backend provisioning on OpenStack.

### 2.1 Create a VM

1. Go to [stack.dhbw.cloud](https://stack.dhbw.cloud/)

2. Configure:

    * **Image**: Ubuntu 22.04
    * **Volume**: No volume
    * **Flavor**: `m1_extra_large` (prod) or `mb1.medium` (dev)
    * **Network**: `provider_912`
    * **Security Group**: Allow inbound (ingress) on ports `22` and `8000`
    * **SSH Key**: Choose a keypair
    * **Init Script**: Upload [`backendscript.yaml`](/backendscript.yaml)

3. Launch the instance.

---

### 2.2 Connect via SSH

```bash
ssh ubuntu@<instance-ip> -i <path-to-private-key>
```

---

### 2.3 Run Initialization Script

```bash
/initilization_script
```

This script installs dependencies, sets up the backend, applies environment configuration, and registers the
app as a system service.

---

### 2.4 Manage Backend with systemd

```bash
sudo systemctl enable eduvmstorebackend
```

```bash
sudo systemctl start eduvmstorebackend
```

```bash
sudo systemctl stop eduvmstorebackend
```

```bash
sudo systemctl restart eduvmstorebackend
```
