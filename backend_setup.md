## Backend DEV Setup and Run
Use the following instructions to set up and run the Backend.
You need to have the repository cloned and be in the main folder of the project to run the commands. This folder is the one that contains the `eduvmstorebackend` folder.
Alternatively you can start a VM using the cloud init script described below.

### Setup Environament and Environment Variables (only once)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Local Database (first time + everytime you change the models.py)
Ensure that the local Database is up to date and ready for use.
```bash
python eduvmstorebackend/manage.py makemigrations
python eduvmstorebackend/manage.py migrate
```
OR 
```bash
python3 eduvmstorebackend/manage.py makemigrations
python3 eduvmstorebackend/manage.py migrate
```
After the commands:
* Double-click the `db.sqlite3` (if this is the first time)
* In the pop-up, click on "Download missing Drivers", wait for the installation to complete, and click "OK"

### Start Backend Server Locally:
```bash
python3 eduvmstorebackend/manage.py runserver 0.0.0.0:8000
```
* Access via `localhost:8000` or if run inside a VM via `<vm-ip>:8000`


### API Access
* Access via `localhost:8000/api/<endpoint>`
* `<endpoint>`: e.g., `<base-url>/app-templates/...`, `<base-url>/users/...`
* You can use the Bruno Endpoints for that:
  * Download Bruno Desktop (https://www.usebruno.com/)
  * Open the folder [APICollectionEduVMStore](/APICollectionEduVMStore) with Bruno
  * Choose/Configure the Environment (IP-Addresses: OpenStack for Authentication und BASE_URL (Backend) and Openstack Username an Password need to be set the first time)
  * Send the authentication request (this sets a variable in Bruno with the authentication token and uses it for all other endpoints)
  * Choose and send the Endpoint you want to test (at some endpoints variables for other endpoints are set)

### Run Tests
Runs the unit tests for the project.
```bash
python eduvmstorebackend/manage.py test
```
OR 
```bash
python3 eduvmstorebackend/manage.py test
```

## Alternative: Use Cloud-Init-Script for faster Setup
* On `https://stack.dhbw.cloud/` create new instance
* At Source choose Image as Boot Source, Ubuntu 22.04 as Image and no new Volume
* Choose your Flavor of choice
* For Network choose provider_912
* The Security Group should allow ingress TCP connections on port 8000 and 22
* Choose your SSH Keypair of choice to access the VM through ssh
* At Configuration upload the Cloud-Init-Script [backendscript.yaml](/backendscript.yaml)
* Launch the Instance
* Access the Instance using `ssh ubuntu@<instance-ip> -i <path-to-keyfile>`
* Execute 
```bash
/initilization_script
```
* To manage the Backend-Service you can use:
```bash
sudo systemctl enable eduvmstorebackend
```
```bash
sudo systemctl start eduvmstorebackend
```
```bash
sudo systemctl stop eduvmstorebackend
````
```bash
sudo systemctl restart eduvmstorebackend
```

