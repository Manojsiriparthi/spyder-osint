import requests
from urllib.parse import urljoin

def zap(main_url, archive, domain, host, internal, robots, proxies):
    """Initial URL processing and robots.txt fetching"""
    
    # Import here to avoid circular imports
    from .config import info, good
    
    print(f'{info} Processing initial URL: {main_url}')
    
    # Fetch robots.txt
    try:
        robots_url = urljoin(main_url, '/robots.txt')
        proxy = proxies[0] if proxies and proxies[0] else None
        response = requests.get(robots_url, proxies=proxy, timeout=10)
        
        if response.status_code == 200:
            print(f'{good} Found robots.txt')
            lines = response.text.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('Disallow:') or line.startswith('Allow:'):
                    path = line.split(':', 1)[1].strip()
                    if path and path != '/':
                        robots.add(path)
                        # Add to internal URLs if it's a valid path
                        if not path.startswith('http'):
                            full_url = urljoin(main_url, path)
                            internal.add(full_url)
    except Exception as e:
        print(f'{info} No robots.txt found or error: {e}')
    
    # Handle Wayback Machine integration (placeholder)
    if archive:
        print(f'{info} Archive.org integration not yet implemented')
