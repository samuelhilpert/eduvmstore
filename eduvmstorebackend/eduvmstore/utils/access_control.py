import logging
from django.urls import resolve
from eduvmstore.config.access_levels import DEFAULT_ACCESS_LEVEL, REQUIRED_ACCESS_LEVELS
from rest_framework.request import Request

logger = logging.getLogger('eduvmstore_logger')
def has_access_level(user, url: str, method: str) ->bool:
    """
    Check if user has sufficient access level for a given operation.

    :param Users user: User to check access for
    :param str url: URL name
    :param str method: HTTP method (GET, POST, etc.)
    :return: True if access is allowed, False otherwise
    :rtype: bool
    """
    logger.debug("Checking access level for user")
    required_level = get_required_access_level(url, method)
    logger.debug(f"required level: {required_level}")
    logger.debug(f"access_level: {user.role_id.access_level}")
    access = user.role_id.access_level >= required_level
    logger.debug(f"after access calculation: {access}")
    if not access:
        logger.error(f'Access denied for user: {user.id}')
    return access


def get_required_access_level(url: str, method: str) ->int:
    """
    Get required access level for an operation.

    :param str url: URL name
    :param str method: HTTP method (GET, POST, etc.)
    :return: Required access level
    :rtype: int
    """
    key = (url, method)
    return REQUIRED_ACCESS_LEVELS.get(key, DEFAULT_ACCESS_LEVEL)

def check_request_access(request: Request) ->bool:
    """
    Check if the user in the request has access to the current URL.

    :param Request request: The request to check
    :return: True if access is allowed, False otherwise
    :rtype: bool
    """
    url_name = resolve(request.path).url_name
    return has_access_level(request.myuser, url_name, request.method)