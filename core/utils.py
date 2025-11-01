import re
import time
import json
import os
import random
from urllib.parse import urlparse
import requests
from .config import verbose, info, good, bad

def luhn(card_number):
    """Validate credit card numbers using Luhn algorithm"""
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10 == 0

def proxy_type(proxy_string):
    """Parse proxy string into dict format"""
    if ':' in proxy_string:
        host, port = proxy_string.split(':', 1)
        return {'http': f'http://{host}:{port}', 'https': f'http://{host}:{port}'}
    return None

def is_good_proxy(proxy):
    """Test if proxy is working"""
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxy, timeout=5)
        return response.status_code == 200
    except:
        return False

def top_level(url, fix_protocol=False):
    """Extract top-level domain from URL"""
    if fix_protocol and not url.startswith('http'):
        url = 'http://' + url
    
    parsed = urlparse(url)
    domain = parsed.netloc
    
    # Extract main domain (remove subdomains)
    parts = domain.split('.')
    if len(parts) >= 2:
        return '.'.join(parts[-2:])
    return domain

def extract_headers(prompt_text):
    """Extract headers from prompt text"""
    headers = {}
    lines = prompt_text.split('\n')
    for line in lines:
        if ':' in line and line.strip():
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()
    return headers

def verb(label, data):
    """Print verbose output"""
    if verbose:
        print(f'{info} {label}: {data}')

def is_link(link, processed, files):
    """Check if URL is a valid link to process"""
    if not link or link in processed:
        return False
    
    # Skip common file extensions
    skip_extensions = ['.css', '.js', '.jpg', '.png', '.gif', '.pdf', '.zip', '.rar']
    for ext in skip_extensions:
        if link.lower().endswith(ext):
            files.add(link)
            return False
    
    return True

def entropy(data):
    """Calculate entropy of string"""
    if len(data) == 0:
        return 0
    
    entropy = 0
    for x in range(256):
        char = chr(x)
        if char in data:
            p_x = float(data.count(char)) / len(data)
            if p_x > 0:
                import math
                entropy += - p_x * math.log2(p_x)
    return entropy

def regxy(pattern, text, suppress, custom_set):
    """Apply custom regex pattern"""
    try:
        matches = re.findall(pattern, text)
        for match in matches:
            custom_set.add(match)
    except Exception as e:
        if not suppress:
            print(f'{bad} Regex error: {e}')

def remove_regex(urls, exclude_pattern):
    """Remove URLs matching exclude pattern"""
    if not exclude_pattern:
        return urls
    
    filtered = set()
    for url in urls:
        if not re.search(exclude_pattern, url):
            filtered.add(url)
    return filtered

def timer(diff, processed):
    """Calculate timing statistics"""
    minutes = int(diff // 60)
    seconds = int(diff % 60)
    time_per_request = diff / len(processed) if len(processed) > 0 else 0
    return minutes, seconds, time_per_request

def writer(datasets, dataset_names, output_dir):
    """Write datasets to files"""
    for dataset, name in zip(datasets, dataset_names):
        if dataset:
            filename = os.path.join(output_dir, f'{name}.txt')
            with open(filename, 'w') as f:
                for item in dataset:
                    f.write(str(item) + '\n')
            print(f'{good} {name.capitalize()} saved to {filename}')
