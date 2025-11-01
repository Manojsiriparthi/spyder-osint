import requests
import random
import time
from urllib.parse import urljoin
from .config import bad, good, info, verbose

def requester(url, main_url, delay, cookie, headers, timeout, host, proxies, user_agents, failed, processed):
    """Make HTTP request and return response text"""
    
    processed.add(url)
    
    if delay:
        time.sleep(delay)
    
    # Select random proxy and user agent
    proxy = random.choice(proxies) if proxies else None
    user_agent = random.choice(user_agents) if user_agents else 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    
    # Prepare headers
    request_headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    if headers:
        request_headers.update(headers)
    
    if cookie:
        request_headers['Cookie'] = cookie
    
    try:
        if verbose:
            print(f'{info} Requesting: {url}')
        
        response = requests.get(
            url,
            headers=request_headers,
            proxies=proxy,
            timeout=timeout,
            allow_redirects=True,
            verify=False
        )
        
        if response.status_code == 200:
            return response.text
        else:
            if verbose:
                print(f'{bad} HTTP {response.status_code}: {url}')
            failed.add(url)
            return ''
            
    except requests.exceptions.RequestException as e:
        if verbose:
            print(f'{bad} Request failed for {url}: {str(e)}')
        failed.add(url)
        return ''
    except Exception as e:
        if verbose:
            print(f'{bad} Unexpected error for {url}: {str(e)}')
        failed.add(url)
        return ''
