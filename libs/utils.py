import json

"""
Utils functions -
"""

def format_dict(data):
    """Format dictionary for display"""
    return json.dumps(data, indent=2)

def proxy_type(proxy_string):
    """Parse proxy string into dictionary format"""
    if ':' in proxy_string:
        host, port = proxy_string.split(':', 1)
        return {
            'http': f'http://{host}:{port}',
            'https': f'https://{host}:{port}'
        }
    return None
