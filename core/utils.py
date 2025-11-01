import re
import os
import json
import math
import time
import requests
from urllib.parse import urlparse
from libs.config import good, info, bad

def luhn(card_number):
    """Validate credit card using Luhn algorithm."""
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_number.replace(' ', '').replace('-', ''))
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

def is_good_proxy(proxy_dict):
    """Test if proxy is working."""
    try:
        response = requests.get(
            'http://httpbin.org/ip',
            proxies=proxy_dict,
            timeout=10
        )
        return response.status_code == 200
    except:
        return False

def top_level(url, fix_protocol=False):
    """Extract top level domain from URL."""
    parsed = urlparse(url)
    domain = parsed.netloc
    if fix_protocol and not parsed.scheme:
        return urlparse(f"http://{url}").netloc
    return domain

def extract_headers(prompt_content):
    """Extract headers from prompt content."""
    headers = {}
    for line in prompt_content.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()
    return headers

def verb(category, data):
    """Verbose output function."""
    from libs.config import verbose, info
    if verbose:
        print(f"{info} {category}: {data}")

def is_link(link, processed, files):
    """Check if link should be processed."""
    if link in processed:
        return False
    
    # Skip common file extensions that aren't crawlable
    skip_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.exe', '.doc', '.docx']
    if any(link.lower().endswith(ext) for ext in skip_extensions):
        files.add(link)
        return False
    
    return True

def entropy(string):
    """Calculate Shannon entropy of a string."""
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy

def regxy(regex_pattern, response, suppress, custom_set):
    """Extract custom regex matches."""
    try:
        pattern = re.compile(regex_pattern, re.IGNORECASE)
        matches = pattern.findall(response)
        for match in matches:
            verb('Custom regex', match)
            custom_set.add(match)
    except re.error as e:
        if not suppress:
            print(f"{bad} Invalid regex pattern: {e}")

def remove_regex(links, exclude_pattern):
    """Remove links matching exclude pattern."""
    if not exclude_pattern:
        return list(links)
    
    pattern = re.compile(exclude_pattern)
    return [link for link in links if not pattern.search(link)]

def timer(diff, processed):
    """Calculate timing statistics."""
    minutes = int(diff // 60)
    seconds = int(diff % 60)
    time_per_request = diff / len(processed) if processed else 0
    return minutes, seconds, time_per_request

def writer(datasets, dataset_names, output_dir):
    """Write datasets to files."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for dataset, name in zip(datasets, dataset_names):
        if dataset:
            filepath = os.path.join(output_dir, f"{name}.txt")
            with open(filepath, 'w') as f:
                for item in dataset:
                    f.write(str(item) + '\n')
            print(f"{good} {name.capitalize()} saved to {filepath}")
