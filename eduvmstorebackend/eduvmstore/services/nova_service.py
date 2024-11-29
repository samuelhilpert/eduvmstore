from .keystone_service import get_openstack_connection

def list_instances(token):
    """
    List all instances (servers) in OpenStack.

    :return: A list of instance names
    :rtype: list[str]
    """
    conn = get_openstack_connection(token=token)
    servers = conn.compute.servers()
    return [server.name for server in servers]

def create_instance(name, image_id, flavor_id, network_id, token):
    """
    Create a new instance (server) in OpenStack.

    :param str name: The name of the new instance
    :param str image_id: The ID of the image to use for the instance
    :param str flavor_id: The ID of the flavor to use for the instance
    :param str network_id: The ID of the network to attach to the instance
    :param str token: The authentication token to use for the request
    :return: The created instance object
    :rtype: object
    """
    conn = get_openstack_connection(token=token)
    try:
        #keypair = create_keypair(conn)

        server = conn.compute.create_server(
            name=name,
            image_id=image_id,
            flavor_id=flavor_id,
            networks=[{"uuid": network_id}],
            key_name="JaredKey",
        )
        print("server: ", server)
        conn.compute.wait_for_server(server)
        return server
    except Exception as e:
        print('Exception: ', e)
        return {}

