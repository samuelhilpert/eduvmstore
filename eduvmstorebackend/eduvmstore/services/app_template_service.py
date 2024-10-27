from django.core.exceptions import ObjectDoesNotExist

from eduvmstore.db.operations.app_templates import get_app_template_by_id
from .keystone_service import get_openstack_connection


def get_image_id_from_app_template(app_template_id):
    try:
        app_template = get_app_template_by_id(app_template_id)
        return app_template.image_id
    except ObjectDoesNotExist:
        raise ValueError("AppTemplate not found")

def get_default_network_id(token):
    conn = get_openstack_connection(token=token)
    networks = list(conn.network.networks())
    if networks:
        return networks[0].id  # Return the first network ID
    else:
        raise ValueError("No networks available")