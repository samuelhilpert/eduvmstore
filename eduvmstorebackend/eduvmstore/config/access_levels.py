REQUIRED_ACCESS_LEVELS = {
    ('app-template-list', 'GET'): 1001,
    ('app-template-check-name-collisions', 'GET'): 1001,
    ('app-template-detail', 'GET'): 1002,
    ('app-template-list', 'POST'): 1101,
    ('app-template-favorites', 'GET'): 1102,
    ('app-template-detail', 'PUT'): 1201,
    ('app-template-detail', 'DELETE'): 1202,
    ("app-template-list-all", "GET"): 3101, #No Endpoint, access to see all AppTemplates
    ('app-template-reject', 'PATCH'): 3102,
    ('app-template-approve', 'PATCH'): 3103,

    ('favorite-list', 'POST'): 1103,
    ('favorite-delete-by-app-template', 'DELETE'): 1104,

    ('user-list', 'GET'): 6001,
    ('user-detail', 'GET'): 1002,
    ('user-list', 'POST'): 6101,
    ('user-detail', 'PUT'): 6201,
    ('user-detail', 'DELETE') : 6202,
    ('user-detail', 'PATCH'): 6301,

    ('role-list', 'GET'): 1,
    ('role-detail', 'GET'): 2,
    ('role-list', 'POST'): 6501,
    ('role-detail', 'PUT'): 6601,
    ('role-detail', 'DELETE'): 6602,
}

DEFAULT_ACCESS_LEVEL = 8000


DEFAULT_ROLES = {
    'EduVMStoreUser': {
        'name': 'EduVMStoreUser',
        'access_level': 2000
    },
    'EduVMStoreAdmin': {
        'name': 'EduVMStoreAdmin',
        'access_level': 7000
    }
}
