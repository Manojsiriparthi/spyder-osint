import re
from urllib.parse import urljoin, urlparse

def rhref(response, main_url, host):
    """Extract href links from HTML response"""
    links = set()
    
    # Various link patterns
    patterns = [
        r'href=["\']([^"\']+)["\']',
        r'src=["\']([^"\']+)["\']',
        r'action=["\']([^"\']+)["\']'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, response, re.IGNORECASE)
        for match in matches:
            if match.startswith(('http://', 'https://')):
                links.add(match)
            elif match.startswith('/'):
                full_url = urljoin(main_url, match)
                links.add(full_url)
            elif not match.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                full_url = urljoin(main_url, match)
                links.add(full_url)
    
    return links

def rintels(response, main_url):
    """Extract intelligence data like emails, phone numbers, etc."""
    intel = set()
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, response)
    intel.update(emails)
    
    # Phone patterns
    phone_patterns = [
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        r'\(\d{3}\)\s*\d{3}[-.]?\d{4}',
        r'\+\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}'
    ]
    
    for pattern in phone_patterns:
        phones = re.findall(pattern, response)
        intel.update(phones)
    
    # IP addresses
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ips = re.findall(ip_pattern, response)
    intel.update(ips)
    
    return intel

def rendpoint(response, main_url):
    """Extract API endpoints and interesting paths"""
    endpoints = set()
    
    # API endpoint patterns
    api_patterns = [
        r'["\']([^"\']*(?:api|endpoint|service|rest)[^"\']*)["\']',
        r'["\']([^"\']*\.json)["\']',
        r'["\']([^"\']*\.xml)["\']',
        r'["\']([^"\']*v\d+[^"\']*)["\']'
    ]
    
    for pattern in api_patterns:
        matches = re.findall(pattern, response, re.IGNORECASE)
        for match in matches:
            if match.startswith('/'):
                full_url = urljoin(main_url, match)
                endpoints.add(full_url)
            elif not match.startswith(('http', '#', 'javascript')):
                endpoints.add(match)
    
    return endpoints

def rscript(response, url):
    """Extract JavaScript files and inline scripts"""
    scripts = set()
    
    # External script files
    script_pattern = r'<script[^>]*src=["\']([^"\']+)["\'][^>]*>'
    matches = re.findall(script_pattern, response, re.IGNORECASE)
    for match in matches:
        if match.startswith('/'):
            full_url = urljoin(url, match)
            scripts.add(full_url)
        elif match.startswith(('http://', 'https://')):
            scripts.add(match)
    
    return scripts

def rentropy(response):
    """Find high entropy strings that might be secrets"""
    from core.utils import entropy
    
    secrets = set()
    
    # Look for potential API keys, tokens, etc.
    patterns = [
        r'["\']([A-Za-z0-9+/]{32,}={0,2})["\']',  # Base64-like strings
        r'["\']([A-Za-z0-9]{32,})["\']',          # Long alphanumeric strings
        r'["\']([a-f0-9]{32,})["\']'              # Hex strings
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, response)
        for match in matches:
            if entropy(match) > 4.5:  # High entropy threshold
                secrets.add(match)
    
    return secrets
