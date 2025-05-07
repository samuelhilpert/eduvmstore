# EduVMStore

## Project Overview

This project involves the development of an **AppStore** for providing applications on an OpenStack platform.
The goal is to enable instructors to deploy applications that can be used by students
in the context of courses without requiring deep knowledge of OpenStack. 
The focus is on automated configuration and easy management.

The frontend repo can be found here: https://github.com/samuelhilpert/eduvmstore-ui. Beware that in this implementation the frontend, being directly integrated in horizon (Openstack), handles a lot of logic.

### Main Features
- **Automated Deployment**: Simplified deployment process with automated steps for configuring VMs,
user accounts, network settings, etc.
- **Support for Various Applications**: The AppStore can provide pre-configured environments
for different applications.

This project is being implemented as part of the "Project" module at DHBW Mannheim
from August 2024 to May 2025.

### Installation and Configuration
For installation and configuration instructions, please refer to 
- Backend Setup: [Backend Setup Guide](backend_setup).
- Frontend Setup/Whole Project Setup : [Setup Guide in Frontend Repository](https://github.com/samuelhilpert/eduvmstore-ui/blob/dev/README.md).
