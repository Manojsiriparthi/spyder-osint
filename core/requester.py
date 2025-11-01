import requests
import random
import time
from urllib.parse import urljoin, urlparse
from libs.config import bad, info

def requester(url, main_url, delay, cook, headers, timeout, host, proxies, user_agents, failed, processed):
    """Make HTTP request with proper error handling and random user agents."""
    try:
        # Add delay between requests
        if delay:
            time.sleep(delay)
        
        # Select random user agent
        user_agent = random.choice(user_agents) if user_agents else 'Spyder-OSINT/1.0'
        
        # Setup headers
        request_headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        
        if headers:
            request_headers.update(headers)
        
        # Setup cookies
        cookies = {}
        if cook:
            for cookie in cook.split(';'):
                if '=' in cookie:
                    key, value = cookie.strip().split('=', 1)
                    cookies[key] = value
        
        # Select proxy
        proxy = random.choice(proxies) if proxies and proxies[0] else None
        
        # Make request
        response = requests.get(
            url,
            headers=request_headers,
            cookies=cookies,
            timeout=timeout,
            proxies=proxy,
            allow_redirects=True,
            verify=False
        )
        
        processed.add(url)
        return response.text
        
    except Exception as e:
        print(f"{bad} Failed to fetch {url}: {str(e)}")
        failed.add(url)
        processed.add(url)
        return ""
