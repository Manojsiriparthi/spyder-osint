import re

# Regex patterns for finding links
rhref = re.compile(r'(href|src)\s*=\s*["\']([^"\']*)["\']', re.IGNORECASE)

# Regex patterns for JavaScript files
rscript = re.compile(r'<script[^>]*src\s*=\s*["\']([^"\']*)["\'][^>]*>', re.IGNORECASE)

# Regex patterns for endpoints in JavaScript
rendpoint = re.compile(r'["\']([/][a-zA-Z0-9_\-./]*)["\']', re.MULTILINE)

# Regex patterns for entropy (potential secrets)
rentropy = re.compile(r'[A-Za-z0-9+/]{20,}', re.MULTILINE)

# Intelligence gathering patterns
rintels = [
    (re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'), 'EMAIL'),
    (re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'), 'CREDIT_CARD'),
    (re.compile(r'\b\d{3}[-.]?\d{2}[-.]?\d{4}\b'), 'SSN'),
    (re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'), 'IP_ADDRESS'),
    (re.compile(r'(?i)\b(?:api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*[\'"]?([a-zA-Z0-9_\-]{16,})[\'"]?'), 'API_KEY'),
]
