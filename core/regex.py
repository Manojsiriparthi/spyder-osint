import re

# Regex for finding links
rhref = re.compile(r'<a[^>]*\s+href\s*=\s*["\']([^"\']*)["\'][^>]*>', re.IGNORECASE)

# Regex for finding script sources
rscript = re.compile(r'<script[^>]*\s+src\s*=\s*["\']([^"\']*)["\'][^>]*>', re.IGNORECASE)

# Regex for finding endpoints in JavaScript
rendpoint = re.compile(r'["\'](((?:[a-zA-Z]{1,10}://|//)[^"\']{1,})|((?:/|\.\./|\./)[^"\']{1,})|([a-zA-Z0-9_\-/]{1,}/[a-zA-Z0-9_\-/]{1,}\.(?:[a-zA-Z]{1,4}|action)(?:[\?|/][^"\']{0,}|))|((?:/|\.\./|\./)[^"\']{1,}))["\']')

# Regex for finding high entropy strings (potential API keys)
rentropy = re.compile(r'["\'][0-9a-zA-Z_\-]{20,}["\']')

# Intelligence extraction regexes
rintels = [
    (re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'), 'EMAIL'),
    (re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b'), 'CREDIT_CARD'),
    (re.compile(r'\b\d{3}-\d{2}-\d{4}\b'), 'SSN'),
    (re.compile(r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'), 'PHONE'),
    (re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'), 'IP_ADDRESS'),
    (re.compile(r'(?:password|passwd|pass)\s*[:=]\s*["\']([^"\']+)["\']', re.IGNORECASE), 'PASSWORD'),
    (re.compile(r'(?:api[_-]?key|apikey)\s*[:=]\s*["\']([^"\']+)["\']', re.IGNORECASE), 'API_KEY'),
    (re.compile(r'(?:secret[_-]?key|secretkey)\s*[:=]\s*["\']([^"\']+)["\']', re.IGNORECASE), 'SECRET_KEY'),
    (re.compile(r'(?:access[_-]?token|accesstoken)\s*[:=]\s*["\']([^"\']+)["\']', re.IGNORECASE), 'ACCESS_TOKEN'),
]
