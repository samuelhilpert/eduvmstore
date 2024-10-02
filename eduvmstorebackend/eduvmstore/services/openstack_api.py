"""
from openstack import connection

# Set up OpenStack connection (replace with your actual credentials)
conn = connection.Connection(
    auth_url='https://openstack.example.com:5000/v3',
    project_name='your_project',
    username='your_user',
    password='your_password',
    region_name='your_region',
    user_domain_name='default',
    project_domain_name='default',
)

def list_images():
    images = conn.image.images()
    return [image.name for image in images]
"""