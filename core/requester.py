import requests
import random
import time

def requester(url, main_url, delay, cookies, headers, timeout, host, proxies, user_agents, failed, processed):
    """Make HTTP request and return response."""
    try:
        time.sleep(delay)
        
        session = requests.Session()
        if cookies:
            session.cookies.update(cookies)
        if headers:
            session.headers.update(headers)
            
        session.headers.update({
            'User-Agent': random.choice(user_agents) if user_agents else 'Mozilla/5.0'
        })
        
        proxy = random.choice(proxies) if proxies else None
        
        response = session.get(url, timeout=timeout, proxies=proxy, verify=False)
        processed.add(url)
        
        return response.text
        
    except Exception as e:
        failed.add(f'{url}: {str(e)}')
        return ''
