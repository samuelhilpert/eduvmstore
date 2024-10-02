from openstack import connection

# Set up OpenStack connection (replace with your actual credentials)
conn = connection.Connection(
    auth_url='https://openstack.example.com:5000/v3',
    project_name='eduvmstore',
    username='admin',
    password='nomoresecret',
    region_name='eu-central',
    user_domain_name='default',
    project_domain_name='default',
)

def list_images():
    return [image.name for image in conn.image.images()]

def create_server(name, image_id, flavor_id, network_id):
    return conn.compute.create_server(
        name=name,
        image_id=image_id,
        flavor_id=flavor_id,
        networks=[{"uuid": network_id}]
    )
