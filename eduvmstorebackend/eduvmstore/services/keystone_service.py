import openstack
from django.conf import settings

def get_openstack_connection():
    """
    Create and return a connection to OpenStack based on Django settings.

    :return: An OpenStack connection object
    :rtype: openstack.connection.Connection
    """
    conn = openstack.connect(
        auth_url=settings.OPENSTACK['auth_url'],
        project_name=settings.OPENSTACK['project_name'],
        username=settings.OPENSTACK['username'],
        password=settings.OPENSTACK['password'],
        user_domain_name=settings.OPENSTACK['user_domain_name'],
        project_domain_name=settings.OPENSTACK['project_domain_name'],
        region_name=settings.OPENSTACK['region_name'],
    )
    return conn
