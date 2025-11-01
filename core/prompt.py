import os

def prompt():
    """Load prompt file for headers"""
    prompt_file = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'headers.txt')
    
    if not os.path.exists(prompt_file):
        # Create default headers prompt
        os.makedirs(os.path.dirname(prompt_file), exist_ok=True)
        default_headers = """User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive"""
        
        with open(prompt_file, 'w') as f:
            f.write(default_headers)
    
    with open(prompt_file, 'r') as f:
        return f.read()
