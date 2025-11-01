import requests
from urllib.parse import urljoin, urlparse
from .config import info, bad, good, verbose

def zap(main_url, archive, domain, host, internal, robots, proxies):
    """Initial URL processing and robots.txt fetching"""
    
    print(f'{info} Initializing crawl for {main_url}')
    
    # Try to fetch robots.txt
    try:
        robots_url = urljoin(main_url, '/robots.txt')
        response = requests.get(robots_url, timeout=10)
        
        if response.status_code == 200:
            print(f'{good} Found robots.txt')
            robots_content = response.text
            
            # Parse robots.txt for URLs
            for line in robots_content.split('\n'):
                line = line.strip()
                if line.startswith('Disallow:') or line.startswith('Allow:'):
                    path = line.split(':', 1)[1].strip()
                    if path and path != '/':
                        full_url = urljoin(main_url, path)
                        robots.add(full_url)
                        if verbose:
                            print(f'{info} Found in robots.txt: {path}')
                            
        else:
            print(f'{info} No robots.txt found')
            
    except Exception as e:
        if verbose:
            print(f'{bad} Error fetching robots.txt: {str(e)}')
    
    # Add common paths to check
    common_paths = [
        '/admin', '/login', '/wp-admin', '/phpmyadmin', 
        '/admin.php', '/administrator', '/wp-login.php',
        '/sitemap.xml', '/sitemap.txt', '/.well-known/',
        '/api', '/v1', '/v2', '/swagger', '/docs'
    ]
    
    for path in common_paths:
        full_url = urljoin(main_url, path)
        robots.add(full_url)
    
    print(f'{info} Added {len(robots)} URLs from robots.txt and common paths')
