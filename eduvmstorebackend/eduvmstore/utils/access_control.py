from django.urls import resolve
from eduvmstore.config.access_levels import DEFAULT_ACCESS_LEVEL, REQUIRED_ACCESS_LEVELS

def has_access_level(user, url, method) ->bool:
    """
    Check if user has sufficient access level for a given operation.

    :param Users user: User to check access for
    :param str url: URL name
    :param str method: HTTP method (GET, POST, etc.)
    :return: True if access is allowed, False otherwise
    :rtype: bool
    """
    required_level = get_required_access_level(url, method)
    return user.role_id.access_level >= required_level


def get_required_access_level(url, method) ->int:
    """
    Get required access level for an operation.

    :param str url: URL name
    :param str method: HTTP method (GET, POST, etc.)
    :return: Required access level
    :rtype: int
    """
    key = (url, method)
    return REQUIRED_ACCESS_LEVELS.get(key, DEFAULT_ACCESS_LEVEL)

def check_request_access(request):
    """
    Check if the user in the request has access to the current URL.

    :param HttpRequest request: The request to check
    :return: True if access is allowed, False otherwise
    :rtype: bool
    """
    url_name = resolve(request.path).url_name
    return has_access_level(request.myuser, url_name, request.method)