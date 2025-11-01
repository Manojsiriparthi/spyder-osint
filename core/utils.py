import re
import os
import json
import csv
import time
from urllib.parse import urlparse

def verb(tag, value):
    """Print verbose output."""
    if verbose:
        print(f'[{tag}] {value}')

def luhn(card_num):
    """Validate credit card using Luhn algorithm."""
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
    """Parse proxy string."""
    return {'http': f'http://{proxy_string}', 'https': f'https://{proxy_string}'}

def is_good_proxy(proxy):
    """Test if proxy is working."""
    return True  # Simplified for demo

def top_level(url, fix_protocol=False):
    """Extract top level domain."""
    parsed = urlparse(url)
    return parsed.netloc

def extract_headers(prompt_text):
    """Extract headers from prompt."""
    return {}

def is_link(link, processed, files):
    """Check if URL is a valid link."""
    return bool(link and link not in processed)

def entropy(string):
    """Calculate entropy of string."""
    import math
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    entropy_val = -sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy_val

def regxy(pattern, response, suppress, custom_set):
    """Find regex patterns in response."""
    matches = re.findall(pattern, response)
    for match in matches:
        custom_set.add(match)

def remove_regex(urls, exclude_pattern):
    """Remove URLs matching exclude pattern."""
    if not exclude_pattern:
        return urls
    return [url for url in urls if not re.search(exclude_pattern, url)]

def timer(diff, processed):
    """Calculate timing statistics."""
    minutes = int(diff // 60)
    seconds = int(diff % 60)
    time_per_request = diff / len(processed) if processed else 0
    return minutes, seconds, time_per_request

def writer(datasets, dataset_names, output_dir):
    """Write datasets to files."""
    for dataset, name in zip(datasets, dataset_names):
        if dataset:
            with open(f'{output_dir}/{name}.txt', 'w') as f:
                for item in dataset:
                    f.write(str(item) + '\n')
