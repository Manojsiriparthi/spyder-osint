import re
import os
import json
import math
import time
import csv
import requests
from urllib.parse import urlparse
from libs.config import good, info, bad

def luhn(card_number):
    """Validate credit card numbers using Luhn algorithm"""
    def luhn_checksum(card_num):
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_num)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return checksum % 10
    
    return luhn_checksum(card_number) == 0

def proxy_type(proxy_string):
    """Parse proxy string into dict format"""
    if ':' in proxy_string:
        host, port = proxy_string.split(':', 1)
        return {'http': f'http://{host}:{port}', 'https': f'http://{host}:{port}'}
    return None

def is_good_proxy(proxy):
    """Test if proxy is working"""
    try:
        response = requests.get('http://httpbin.org/ip', 
                              proxies=proxy, timeout=10)
        return response.status_code == 200
    except:
        return False

def top_level(url):
    """Extract top level domain from URL"""
    try:
        parsed = urlparse(url)
        domain_parts = parsed.netloc.split('.')
        if len(domain_parts) >= 2:
            return f"{domain_parts[-2]}.{domain_parts[-1]}"
        return parsed.netloc
    except:
        return ""

def extract_headers(response):
    """Extract interesting headers from HTTP response"""
    interesting_headers = [
        'server', 'x-powered-by', 'x-frame-options',
        'content-security-policy', 'x-content-type-options'
    ]
    
    extracted = {}
    for header in interesting_headers:
        value = response.headers.get(header)
        if value:
            extracted[header] = value
    
    return extracted

def verb(message, verbose):
    """Print verbose message if verbose mode is enabled"""
    if verbose:
        print(f"[VERBOSE] {message}")

def is_link(url, main_url):
    """Check if URL is a valid link"""
    try:
        parsed = urlparse(url)
        return parsed.scheme in ['http', 'https'] and parsed.netloc
    except:
        return False

def entropy(string):
    """Calculate Shannon entropy of a string"""
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    entropy_val = -sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy_val

def regxy(response, pattern):
    """Apply custom regex pattern to response"""
    try:
        matches = re.findall(pattern, response, re.IGNORECASE)
        return set(matches) if matches else set()
    except:
        return set()

def remove_regex(data, pattern):
    """Remove items matching regex pattern"""
    try:
        compiled_pattern = re.compile(pattern)
        return {item for item in data if not compiled_pattern.search(item)}
    except:
        return data

def timer(start_time):
    """Calculate elapsed time"""
    return time.time() - start_time

def writer(data, export_format, output_dir):
    """Write data to file in specified format"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = int(time.time())
    
    if export_format == 'json':
        filename = os.path.join(output_dir, f'spyder_results_{timestamp}.json')
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=list)
    
    elif export_format == 'csv':
        filename = os.path.join(output_dir, f'spyder_results_{timestamp}.csv')
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Type', 'Data'])
            for key, values in data.items():
                for value in values:
                    writer.writerow([key, value])
    
    return filename

def format_dict(data):
    """Format dictionary for pretty printing"""
    formatted = {}
    for key, value in data.items():
        if isinstance(value, set):
            formatted[key] = list(value)
        else:
            formatted[key] = value
    return formatted
