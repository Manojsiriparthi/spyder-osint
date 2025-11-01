import os
from urllib.parse import urlparse, unquote
from .config import info, bad, good

def mirror(url, response):
    """Save website content locally"""
    try:
        parsed_url = urlparse(url)
        path = parsed_url.path
        
        if not path or path == '/':
            path = '/index.html'
        
        # Remove leading slash and decode
        local_path = unquote(path.lstrip('/'))
        
        # Create directory structure
        dir_path = os.path.dirname(local_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        
        # Write file
        with open(local_path, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(response)
            
    except Exception as e:
        print(f'{bad} Mirror error for {url}: {str(e)}')
