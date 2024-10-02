from .keystone_service import get_openstack_connection

def list_instances():
    """List all instances (servers) in OpenStack."""
    conn = get_openstack_connection()
    servers = conn.compute.servers()
    return [server.name for server in servers]

def create_instance(name, image_id, flavor_id, network_id):
    """Create a new instance (server) in OpenStack."""
    conn = get_openstack_connection()
    server = conn.compute.create_server(
        name=name,
        image_id=image_id,
        flavor_id=flavor_id,
        networks=[{"uuid": network_id}],
    )
    conn.compute.wait_for_server(server)
    return server
