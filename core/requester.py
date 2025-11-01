import requests
import random
import time
from urllib.parse import urljoin

def requester(url, main_url, delay, cookies, headers, timeout, host, proxies, user_agents, failed, processed):
    """Make HTTP requests with error handling and retries"""
    
    # Import here to avoid circular imports
    from .config import bad, info
    
    processed.add(url)
    
    if delay:
        time.sleep(delay)
    
    # Select random user agent and proxy
    user_agent = random.choice(user_agents) if user_agents else 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    proxy = random.choice(proxies) if proxies and proxies[0] is not None else None
    
    # Set up headers
    req_headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Referer': main_url
    }
    
    if headers:
        req_headers.update(headers)
    
    # Set up cookies
    cookie_dict = None
    if cookies:
        cookie_dict = {}
        for cookie in cookies.split(';'):
            if '=' in cookie:
                name, value = cookie.strip().split('=', 1)
                cookie_dict[name] = value
    
    try:
        response = requests.get(
            url,
            headers=req_headers,
            cookies=cookie_dict,
            proxies=proxy,
            timeout=timeout,
            verify=False,
            allow_redirects=True
        )
        
        if response.status_code == 200:
            return response.text
        else:
            failed.add(f"{url} - Status: {response.status_code}")
            return ""
            
    except Exception as e:
        failed.add(f"{url} - Error: {str(e)}")
        print(f'{bad} Failed to request {url}: {str(e)}')
        return ""
