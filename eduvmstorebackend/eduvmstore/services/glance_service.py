from .keystone_service import get_openstack_connection

def list_images():
    """List all images in OpenStack."""
    conn = get_openstack_connection()
    images = conn.image.images()
    return [image.name for image in images]

def get_image(image_id):
    """Get details of a specific image."""
    conn = get_openstack_connection()
    image = conn.image.get_image(image_id)
    return image
