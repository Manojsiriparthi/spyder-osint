import re

# HTML href extraction pattern  
rhref = re.compile(r'<a [^>]*href=["\']([^"\']*)["\'][^>]*>', re.IGNORECASE)

# Script source extraction pattern
rscript = re.compile(r'<script[^>]*src=["\']([^"\']*)["\'][^>]*>', re.IGNORECASE)

# Endpoint extraction pattern
rendpoint = re.compile(r'["\'](((?:[a-zA-Z]{1,10}://|//)[^"\']{1,}\.[a-zA-Z]{2,}[^"\']{0,})|(((?:/|\.\./|\./)[^"\'><,;|*()(%%$^/\\\[\]][^"\'><,;|()]{1,})))["\']')

# High entropy strings (potential secrets)
rentropy = re.compile(r'[A-Za-z0-9+/]{20,}')

# Intelligence extraction patterns
rintels = [
    (re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'), 'EMAIL'),
    (re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b'), 'CREDIT_CARD'),
    (re.compile(r'\b\d{3}-\d{2}-\d{4}\b'), 'SSN'),
    (re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'), 'IP_ADDRESS'),
    (re.compile(r'\b[A-Za-z0-9]{32}\b'), 'MD5_HASH'),
    (re.compile(r'\b[A-Za-z0-9]{40}\b'), 'SHA1_HASH'),
    (re.compile(r'\b[A-Za-z0-9]{64}\b'), 'SHA256_HASH'),
    (re.compile(r'sk-[A-Za-z0-9]{48}'), 'OPENAI_API_KEY'),
    (re.compile(r'xox[baprs]-[A-Za-z0-9-]+'), 'SLACK_TOKEN'),
    (re.compile(r'ghp_[A-Za-z0-9]{36}'), 'GITHUB_TOKEN'),
]
