import openstack
from django.conf import settings

def get_openstack_connection(token):
    """
    Create and return a connection to OpenStack using the provided token.

    :param str token: The OpenStack token for authentication
    :return: An OpenStack connection object
    :rtype: openstack.connection.Connection
    """
    conn = openstack.connection.Connection(
        auth=dict(
            auth_url=settings.OPENSTACK['auth_url'],
            token=token,
            project_id=settings.OPENSTACK['project_id']
        ),
        verify=settings.OPENSTACK.get('verify_ssl', True)
    )
    return conn
