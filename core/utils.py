import re
import os
import json
import csv
import math
import random
import requests
from urllib.parse import urlparse
from .config import bad, good, info

def luhn(card_num):
    """Validate credit card number using Luhn algorithm"""
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_num)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10 == 0

def proxy_type(proxy_string):
    """Parse proxy string and return proxy dict"""
    if '://' in proxy_string:
        return {'http': proxy_string, 'https': proxy_string}
    else:
        return {'http': f'http://{proxy_string}', 'https': f'http://{proxy_string}'}

def is_good_proxy(proxy_dict):
    """Test if proxy is working"""
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxy_dict, timeout=10)
        return response.status_code == 200
    except:
        return False

def top_level(url, fix_protocol=False):
    """Extract top level domain from URL"""
    try:
        if fix_protocol and not url.startswith('http'):
            url = 'http://' + url
        parsed = urlparse(url)
        domain = parsed.netloc
        parts = domain.split('.')
        if len(parts) >= 2:
            return '.'.join(parts[-2:])
        return domain
    except:
        return url

def extract_headers(prompt_text):
    """Extract headers from prompt text"""
    headers = {}
    lines = prompt_text.split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()
    return headers

def verb(category, data):
    """Verbose output function"""
    from .config import verbose, info
    if verbose:
        print(f'{info} {category}: {data}')

def is_link(link, processed, files):
    """Check if link should be processed"""
    if not link or link in processed:
        return False
    
    # Skip common file extensions that aren't useful for crawling
    skip_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.tar', '.gz']
    for ext in skip_extensions:
        if link.lower().endswith(ext):
            files.add(link)
            return False
    
    return True

def entropy(string):
    """Calculate Shannon entropy of a string"""
    if not string:
        return 0
    entropy = 0
    for x in set(string):
        p_x = float(string.count(x)) / len(string)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

def regxy(pattern, response, suppress, custom_set):
    """Extract custom regex patterns from response"""
    try:
        matches = re.findall(pattern, response)
        for match in matches:
            verb('Custom', match)
            custom_set.add(match)
    except Exception as e:
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

def timer(seconds, processed):
    """Calculate timing statistics"""
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    if len(processed) > 0:
        time_per_request = seconds / len(processed)
    else:
        time_per_request = 0
    return minutes, remaining_seconds, time_per_request

def writer(datasets, names, output_dir):
    """Write datasets to files"""
    for dataset, name in zip(datasets, names):
        if dataset:
            filepath = os.path.join(output_dir, f'{name}.txt')
            with open(filepath, 'w', encoding='utf-8') as f:
                for item in dataset:
                    f.write(str(item) + '\n')
            print(f'{good} {name.capitalize()} saved to {filepath}')
