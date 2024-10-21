from .keystone_service import get_openstack_connection

def list_images():
    """
    List all images in OpenStack.

    :return: A list of accessible OpenStack images (currently only names)
    :rtype: list[str]
    """
    conn = get_openstack_connection()
    images = conn.image.images()
    return [image.name for image in images]

def get_image(image_id):
    """
    Get details of a specific image.

    :param str image_id: The unique identifier of the image
    :return: The image object
    :rtype: object
    """
    conn = get_openstack_connection()
    image = conn.image.get_image(image_id)
    return image
