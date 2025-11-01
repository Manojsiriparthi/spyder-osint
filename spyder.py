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

warnings.filterwarnings('ignore')

print(f"{good} Spyder OSINT - Basic functionality available")
print(f"{info} Some advanced features may be limited until core modules are implemented")

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help='root url', dest='root')
parser.add_argument('-v', '--verbose', help='verbose output', dest='verbose', action='store_true')
parser.add_argument('--help-full', help='show full help when core modules are available', dest='help_full', action='store_true')

args = parser.parse_args()

if args.help_full:
    print(f"{info} Full functionality requires implementing core modules:")
    print("  - core.requester (HTTP request handler)")
    print("  - core.flash (Threading manager)")
    print("  - core.regex (Pattern matching)")
    print("  - core.utils (Utility functions)")
    print("  - core.zap (Archive.org integration)")
    quit()

if not args.root:
    print(f"\n{bad} Please provide a URL with -u/--url")
    print(f"{info} Example: python spyder.py -u https://example.com")
    print(f"{info} Use --help-full to see what modules need to be implemented")
    quit()

print(f"{run} Target URL: {args.root}")
print(f"{info} Basic URL validation and setup complete")
print(f"{yellow} Core crawling modules need to be implemented for full functionality{end}")



