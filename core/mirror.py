import os
from urllib.parse import urlparse
from .config import info, bad, good

def mirror(url, response):
    """Save webpage content locally"""
    
    try:
        parsed_url = urlparse(url)
        
        # Create directory structure
        path_parts = parsed_url.path.strip('/').split('/')
        if not path_parts or path_parts == ['']:
            filename = 'index.html'
            dir_path = 'mirror'
        else:
            filename = path_parts[-1] if '.' in path_parts[-1] else 'index.html'
            dir_path = os.path.join('mirror', *path_parts[:-1]) if len(path_parts) > 1 else 'mirror'
        
        # Ensure filename has extension
        if '.' not in filename:
            filename += '.html'
        
        # Create directories
        os.makedirs(dir_path, exist_ok=True)
        
        # Save file
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(response)
        
        print(f'{good} Mirrored: {url} -> {filepath}')
        
    except Exception as e:
        print(f'{bad} Mirror error for {url}: {str(e)}')
