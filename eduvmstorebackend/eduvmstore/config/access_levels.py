REQUIRED_ACCESS_LEVELS = {
    'GET /app-templates': 1003,
    'GET /app-templates?search={query}': 1004,
    'GET /app-templates?public={public}&approved={approved}': 3001,
    'GET /app-templates/{id}': 1005,
    'POST /app-templates': 1101,
    'PUT /app-templates/{id}': 1102,
    'DELETE /app-templates/{id}': 1103,
    'PATCH /app-templates/{id}/approved': 3101,
    'GET /app-templates/name/{name}/collisions': 1008,
    'GET /users': 6001,
    'GET /users/{id}': 1000,
    'PATCH /users/{id}/': 6101,
    'DELETE /users/{id}': 6102,
    'GET /images': 1001,
    'GET /images/{id}': 1002,
    'POST /flavors/selection': 1006,
    'POST /instances/launch/': 1007,
}


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
