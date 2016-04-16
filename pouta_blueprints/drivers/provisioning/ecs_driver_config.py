CONFIG = {
    'schema': {
        'type': 'object',
        'title': 'Comment',
        'description': 'Description',
        'required': [
            'name',
            'task_definition',
        ],
        'properties': {
            'name': {
                'type': 'string'
            },
            'description': {
                'type': 'string'
            },
            'memory_limit': {
                'type': 'string',
                'default': '512m',
            },
            'access_type': {
                'type': 'string',
                'default': 'raw',
            },
            'consumed_slots': {
                'type': 'integer',
                'default': '1',
            },
            'maximum_instances_per_user': {
                'type': 'integer',
                'title': 'Maximum instances per user',
                'default': 1,
            },
            'maximum_lifetime': {
                'type': 'string',
                'title': 'Maximum life-time (days hours mins)',
                'default': '1h 0m',
                'pattern': '^(\d+d\s?)?(\d{1,2}h\s?)?(\d{1,2}m\s?)?$',
                'validationMessage': 'Value should be in format [days]d [hours]h [minutes]m'
            },
            'task_definition': {
                'type': 'string',
                'title': 'ECS Task definition'
            },
            'cost_multiplier': {
                'type': 'number',
                'title': 'Cost multiplier (default 1.0)',
                'default': 1.0,
            },
            'needs_ssh_keys': {
                'type': 'boolean',
                'title': 'Needs ssh-keys to access',
                'default': False,
            },
            'proxy_options': {
                'type': 'object',
                'title': 'Proxy Options',
                'properties': {
                    'proxy_rewrite': {
                        'type': 'boolean',
                        'title': 'Rewrite the proxy url',
                        'default': False,
                    },
                    'proxy_redirect': {
                        'type': 'boolean',
                        'title': 'Redirect the proxy url',
                        'default': False,
                    },
                    'set_host_header': {
                        'type': 'boolean',
                        'title': 'Set host header',
                        'default': False,
                    }
                }
            },
            'environment_vars': {
                'type': 'string',
                'title': 'environment variables for docker, separated by space',
                'default': '',
            },
        }
    },
    'form': [
        {
            'type': 'help',
            'helpvalue': '<h4>ECS containerconfig</h4>'
        },
        'name',
        'description',
        'task_definition',
        'access_type',
        'consumed_slots',
        'maximum_instances_per_user',
        'maximum_lifetime',
        'cost_multiplier',
        'proxy_options'
    ],
    'model': {
        'name': 'My ECS blueprint',
        'description': 'ECS blueprint',
        'task_definition': 'myTaskDefinition',
        'memory_limit': '512m',
        'cost_multiplier': 0.0,
        'consumed_slots': 1,
        'needs_ssh_keys': False,
        'proxy_options': {
            'proxy_rewrite': True,
            'proxy_redirect': True,
            'set_host_header': False
        }
    }
}
