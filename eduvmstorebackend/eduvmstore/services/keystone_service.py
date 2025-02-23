#import openstack
from django.conf import settings

def get_openstack_connection(token):
    """
    Create and return a connection to OpenStack using the provided token.

    :param str token: The OpenStack token for authentication
    :return: An OpenStack connection object
    :rtype: openstack.connection.Connection
    """
    # try:
    #     conn = openstack.connection.Connection(
    #         region_name='RegionOne',
    #         auth=dict(
    #             auth_url=settings.OPENSTACK['auth_url'],
    #             #token=token,
    #             username='admin',
    #             password='nomoresecret',
    #             project_id=settings.OPENSTACK['project_id'],
    #             user_domain_name='default',
    #             project_domain_name='default',
    #         ),
    #         compute_api_version='2.1',
    #         identity_interface='public',
    #     )
    # except Exception as e:
    #     print('error', e)
    #
    # print('connection', conn)
    # return conn
    return None