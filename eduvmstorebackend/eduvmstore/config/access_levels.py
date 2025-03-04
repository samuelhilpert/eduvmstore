REQUIRED_ACCESS_LEVELS = {
    ('app-template-list', 'GET'): 1001,
    ('app-template-check-name-collisions', 'GET'): 1001,
    ('app-template-detail', 'GET'): 1002,
    ('app-template-list', 'POST'): 1101,
    ('app-template-detail', 'PUT'): 1201,
    ('app-template-detail', 'DELETE'): 1202,
    ('app-template-approved', 'PATCH'): 3101,

    ('user-list', 'GET'): 6001,
    ('user-detail', 'GET'): 1002,
    ('user-list', 'POST'): 6101,
    ('user-detail', 'PUT'): 6201,
    ('user-detail', 'DELETE') : 6202,
    ('user-change-role', 'PATCH'): 6301,

    ('role-list', 'GET'): 1,
    ('role-detail', 'GET'): 2,
    ('role-list', 'POST'): 6501,
    ('role-detail', 'PUT'): 6601,
    ('role-detail', 'DELETE'): 6602,
}

DEFAULT_ACCESS_LEVEL = 8000


DEFAULT_ROLES = {
    'User': {
        'name': 'User',
        'access_level': 2000
    },
    'Admin': {
        'name': 'Admin',
        'access_level': 7000
    }
}
