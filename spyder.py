import asyncio 
import os
import subprocess
import argparse
import warnings
import requests
import random
import sys
import time
import re

try:
    from urllib.parse import urlparse
except ImportError:
    print('Spyder runs only on Python 3.2 and above.')
    quit()

# Use existing libs config instead of core.config
from libs.config import *
from libs.utils import format_dict, proxy_type

# Now import the core modules
try:
    from core.requester import requester
    from core.flash import flash
    from core.regex import rintels, rendpoint, rhref, rscript, rentropy
    from core.utils import (luhn, is_good_proxy, top_level, extract_headers, 
                           verb, is_link, entropy, regxy, remove_regex, timer, writer)
    from core.zap import zap
    
    print(f"{good} Spyder OSINT - All core modules loaded successfully")
    CORE_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"{bad} Missing core module: {e}")
    print(f"{info} Please ensure all core modules are created in the core/ directory")
    CORE_MODULES_AVAILABLE = False

warnings.filterwarnings('ignore')

print(f"{good} Spyder OSINT - Basic functionality available")
print(f"{info} Some advanced features may be limited until core modules are implemented")

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help='root url', dest='root')
parser.add_argument('-c', '--cookie', help='cookie', dest='cook')
parser.add_argument('-r', '--regex', help='regex pattern', dest='regex')
parser.add_argument('-e', '--export', help='export format', dest='export', choices=['csv', 'json'])
parser.add_argument('-o', '--output', help='output directory', dest='output')
parser.add_argument('-l', '--level', help='levels to crawl', dest='level', type=int)
parser.add_argument('-t', '--threads', help='number of threads', dest='threads', type=int)
parser.add_argument('-d', '--delay', help='delay between requests', dest='delay', type=float)
parser.add_argument('-v', '--verbose', help='verbose output', dest='verbose', action='store_true') 
parser.add_argument('-s', '--seeds', help='additional seed URLs', dest='seeds', nargs="+", default=[])
parser.add_argument('--stdout', help='send variables to stdout', dest='std')
parser.add_argument('--user-agent', help='custom user agent(s)', dest='user_agent')
parser.add_argument('--exclude', help='exclude URLs matching this regex', dest='exclude')
parser.add_argument('--timeout', help='http request timeout', dest='timeout', type=float)
parser.add_argument('-p', '--proxy', help='Proxy server IP:PORT or DOMAIN:PORT', dest='proxies', type=proxy_type)
parser.add_argument('--clone', help='clone the website locally', dest='clone', action='store_true')
parser.add_argument('--headers', help='add headers', dest='headers', action='store_true')
parser.add_argument('--dns', help='enumerate subdomains and DNS data', dest='dns', action='store_true')
parser.add_argument('--keys', help='find secret keys', dest='api', action='store_true')
parser.add_argument('--only-urls', help='only extract URLs', dest='only_urls', action='store_true')
parser.add_argument('--wayback', help='fetch URLs from archive.org as seeds', dest='archive', action='store_true')

args = parser.parse_args()

if not CORE_MODULES_AVAILABLE:
    print(f"{bad} Core modules not available. Please create the missing modules:")
    print(f"{info} - core/flash.py (main crawling engine)")
    print(f"{info} - core/regex.py (regex patterns)")  
    print(f"{info} - core/utils.py (utility functions)")
    print(f"{info} - core/requester.py (HTTP requester)")
    print(f"{info} - core/zap.py (initial processing)")
    if args.root:
        print(f"{info} Target: {args.root}")
    sys.exit(1)

if not args.root:
    print(f"\n{bad} Please provide a URL with -u/--url")
    print(f"{info} Example: python spyder.py -u https://example.com")
    print(f"{info} Use --help-full to see what modules need to be implemented")
    quit()

print(f"{run} Target URL: {args.root}")
print(f"{info} Basic URL validation and setup complete")
print(f"{yellow} Core crawling modules need to be implemented for full functionality{end}")

# Add main execution logic
if args.root:
    start_time = time.time()
    
    # Initialize data structures
    failed = set()
    processed = set()
    internal = set()
    external = set()
    files = set()
    intel = set()
    robots = set()
    custom = set()
    scripts = set()
    
    # Parse domain info
    parsed_url = urlparse(args.root)
    host = parsed_url.netloc
    domain = top_level(args.root) if CORE_MODULES_AVAILABLE else parsed_url.netloc
    
    # Set defaults
    level = args.level or 2
    delay = args.delay or 0
    timeout = args.timeout or 10
    threads = args.threads or 10
    
    # Setup user agents
    user_agents = []
    if args.user_agent:
        user_agents = [args.user_agent]
    else:
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
    
    # Initial processing
    zap(args.root, args.archive, domain, host, internal, robots, args.proxies or [])
    
    # Main crawling
    flash(args.root, args.cook, None, timeout, host, args.proxies or [], 
          user_agents, failed, processed, internal, external, files, 
          intel, robots, custom, scripts, level, delay, args.regex, args.exclude)
    
    # Results
    elapsed = timer(start_time)
    print(f"\n{good} Crawling completed in {elapsed:.2f} seconds")
    print(f"{info} Internal URLs: {len(internal)}")
    print(f"{info} External URLs: {len(external)}")
    print(f"{info} Files found: {len(files)}")
    print(f"{info} Intelligence data: {len(intel)}")
    print(f"{info} Scripts found: {len(scripts)}")
    
    # Export results if requested
    if args.export and args.output:
        results = {
            'internal_urls': internal,
            'external_urls': external,
            'files': files,
            'intelligence': intel,
            'scripts': scripts,
            'custom': custom
        }
        
        filename = writer(results, args.export, args.output)
        print(f"{good} Results exported to: {filename}")



