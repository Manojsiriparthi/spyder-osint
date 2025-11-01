import os

def prompt():
    """Load headers prompt from file"""
    
    prompt_file = os.path.join(os.path.dirname(__file__), 'headers.txt')
    
    if not os.path.exists(prompt_file):
        # Create default headers file
        default_headers = """User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive"""
        
        with open(prompt_file, 'w') as f:
            f.write(default_headers)
    
    with open(prompt_file, 'r') as f:
        return f.read()
