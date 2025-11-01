# 📁 Spyder OSINT - Clean Project Structure

## Core Files
```
spyder-osint/
├── main.py                    # Main application entry point
├── requirements.txt           # Essential dependencies only
├── README.md                 # Complete documentation
├── .gitignore                # Git ignore patterns
├── setup.sh                  # Environment setup script
├── run.sh                    # Application runner
├── clean.sh                  # Repository cleanup script
└── project_structure.md      # This file
```

## Modules Directory
```
modules/
├── __init__.py               # Module initialization
├── person_search.py          # Person information gathering
├── phone_search.py           # Phone number investigation
├── email_search.py           # Email analysis
├── social_media_search.py    # Social media discovery
└── image_search.py           # Image and photo search
```

## Utilities Directory
```
utils/
├── __init__.py               # Utilities initialization
├── web_scraper.py            # HTTP request handler
├── display.py                # Result formatting and display
└── data_manager.py           # Data storage and export
```

## Auto-Generated Directories
```
results/                      # Investigation results (auto-created)
├── investigation_*.json      # JSON result files
└── .gitkeep                 # Keep directory in git

venv/                        # Virtual environment (auto-created)
└── (Python virtual environment files)
```

## Excluded Files (in .gitignore)
- Python cache files (`__pycache__/`, `*.pyc`)
- Virtual environment files (`venv/`, `env/`)
- IDE configuration (`.vscode/`, `.idea/`)
- Results and logs (`*.json`, `*.log`)
- OS files (`.DS_Store`, `Thumbs.db`)
- Temporary files (`*.tmp`, `*.temp`)

## Essential Dependencies Only
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `lxml` - XML/HTML parser
- `urllib3` - HTTP client
- `colorama` - Terminal colors

## Removed Dependencies
❌ Unnecessary packages removed:
- `argparse` (built-in Python)
- `certifi` (included with requests)
- `openpyxl` (Excel files - not needed)
- `pandocfilters` (document conversion - not needed)
- `better-proxy` (proxy handling - not needed for basic version)
- `websockets` (WebSocket support - not needed)
- `loguru` (advanced logging - not needed)
- `phonenumbers` (phone parsing - basic regex sufficient)
- `pillow` (image processing - not needed for basic version)
- `aiohttp` (async HTTP - not needed for synchronous version)

This clean structure focuses on core OSINT functionality while maintaining simplicity and ease of use.
