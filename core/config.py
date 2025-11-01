# Configuration settings for Spyder OSINT

verbose = False

# Intelligence sources
INTELS = [
    'github.com',
    'pastebin.com',
    'twitter.com',
    'facebook.com',
    'linkedin.com',
    'instagram.com'
]

# Color codes
red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
blue = '\033[94m'
end = '\033[0m'

# Status indicators
info = f'{blue}[i]{end}'
good = f'{green}[+]{end}'
bad = f'{red}[-]{end}'
run = f'{yellow}[~]{end}'
