# 🕷️ Spyder OSINT - Advanced Person Intelligence Gathering

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/spyder-osint/spyder-osint.svg)](https://github.com/spyder-osint/spyder-osint/issues)

## 📋 Description

Spyder OSINT is a comprehensive Open Source Intelligence (OSINT) tool designed for gathering publicly available information about individuals. This tool aggregates data from multiple sources including social media platforms, search engines, phone directories, and image repositories.

⚠️ **LEGAL DISCLAIMER**: This tool is for educational and legitimate investigative purposes only. Users must comply with local laws and obtain proper authorization before conducting investigations.

## ✨ Features

- **👤 Person Search**: Full name, location, relatives, occupations
- **📞 Phone Investigation**: Carrier info, associated names, addresses
- **📧 Email Analysis**: Account associations, breach data, social profiles
- **📱 Social Media Discovery**: Facebook, Twitter, LinkedIn, Instagram, TikTok, YouTube
- **📸 Image Search**: Profile pictures, Google Photos, social media images
- **🔍 Multi-Engine Search**: Google, Bing, DuckDuckGo integration
- **📊 Structured Output**: JSON export with organized results
- **🛡️ Privacy Focused**: Rate limiting and respectful scraping

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Internet connection

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/spyder-osint/spyder-osint.git
cd spyder-osint

# Install required dependencies
pip install -r requirements.txt

# Make the main script executable
chmod +x main.py
```

### Dependencies Installation

```bash
pip install requests beautifulsoup4 lxml urllib3
```

## 📖 Usage

### Basic Usage

```bash
python3 main.py
```

### Interactive Mode

The application will prompt you for the following information:

1. **Full Name** (Required): Target's complete name
2. **Phone Number** (Optional): Phone number for investigation
3. **Email** (Optional): Email address for analysis
4. **Location** (Optional): City/State for refined search

### Command Line Example

```bash
$ python3 main.py

    ███████╗██████╗ ██╗   ██╗██████╗ ███████╗██████╗ 
    ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
    ███████╗██████╔╝ ╚████╔╝ ██║  ██║█████╗  ██████╔╝
    ╚════██║██╔═══╝   ╚██╔╝  ██║  ██║██╔══╝  ██╔══██╗
    ███████║██║        ██║   ██████╔╝███████╗██║  ██║
    ╚══════╝╚═╝        ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
                    
                    OSINT Intelligence Gathering
                    Version 2.0 | github.com/spyder-osint

============================================================
SPYDER OSINT - Person Intelligence Gathering
============================================================
Enter full name: John Smith
Enter phone number (optional): +1-555-123-4567
Enter email (optional): john.smith@email.com
Enter location/city (optional): New York

[+] Starting OSINT investigation...
```

## 📊 Sample Output

### Personal Information Results

```
================================================================================
INVESTIGATION RESULTS
================================================================================

📋 PERSONAL INFORMATION
----------------------------------------
Name: John Smith
Location: New York

🏠 Possible Addresses:
  • 123 Main Street, New York, NY 10001
  • 456 Broadway Ave, Manhattan, NY 10012
  • 789 Central Park West, NY 10025

👨‍👩‍👧‍👦 Possible Relatives:
  • Mary Smith (wife)
  • Michael Smith (son)
  • Sarah Johnson (sister)

💼 Occupation Information:
  • Works at ABC Corporation as Senior Manager
  • Previously employed by XYZ Tech Company
  • LinkedIn profile shows 10+ years in finance
```

### Phone Investigation Results

```
📞 PHONE INFORMATION
----------------------------------------
Number: +1-555-123-4567
Location: New York, NY (Area Code: 555)
Carrier: Verizon Wireless

👤 Associated Names:
  • John Smith
  • J. Smith
  • John M. Smith
  • Smith Family

🏠 Associated Addresses:
  • 123 Main St, New York, NY 10001
  • 456 Second Ave, NYC, NY 10003
```

### Social Media Discovery

```
📱 SOCIAL MEDIA ACCOUNTS
----------------------------------------

FACEBOOK:
  • John Smith (NYC)
    URL: https://facebook.com/john.smith.nyc
  • John M. Smith
    URL: https://facebook.com/johnmsmith

LINKEDIN:
  • John Smith - Senior Manager at ABC Corp
    URL: https://linkedin.com/in/johnsmith-abc

TWITTER:
  • @JohnSmithNYC
    Display Name: John Smith
  • @JSmith_Finance
    Display Name: J. Smith - Finance Pro

INSTAGRAM:
  • johnsmith_nyc (John Smith)
  • jsmith_photos (J. Smith)
```

### Image Search Results

```
📸 FOUND IMAGES
----------------------------------------

Google Images: 15 images
Bing Images: 12 images  
Profile Pictures: 8 images
Social Media Photos: 23 images

Total images found: 58
Note: Image URLs saved to results file
```

### Email Analysis Results

```
📧 EMAIL INFORMATION
----------------------------------------
Email: john.smith@email.com
Domain: email.com
Valid: Yes

🔗 Associated Accounts:
  • Facebook account linked
  • LinkedIn professional profile
  • Twitter account verified
  • GitHub developer profile

🚨 Security Breaches:
  • Found in 2019 data breach (Company XYZ)
  • Compromised in 2021 social media leak
```

## 📁 Output Files

### JSON Export Sample

```json
{
  "timestamp": "2024-01-15 14:30:25",
  "target": "John Smith",
  "person": {
    "name": "John Smith",
    "location": "New York",
    "possible_addresses": [
      "123 Main Street, New York, NY 10001",
      "456 Broadway Ave, Manhattan, NY 10012"
    ],
    "relatives": [
      "Mary Smith (wife)",
      "Michael Smith (son)"
    ],
    "occupations": [
      "Senior Manager at ABC Corporation",
      "Finance Professional with 10+ years experience"
    ]
  },
  "social": {
    "facebook": [
      {
        "name": "John Smith (NYC)",
        "url": "https://facebook.com/john.smith.nyc",
        "platform": "facebook"
      }
    ],
    "linkedin": [
      {
        "name": "John Smith",
        "title": "Senior Manager at ABC Corp",
        "url": "https://linkedin.com/in/johnsmith-abc",
        "platform": "linkedin"
      }
    ]
  },
  "images": {
    "google_images": [
      {
        "url": "https://example.com/image1.jpg",
        "alt": "John Smith profile photo",
        "source": "google"
      }
    ]
  }
}
```

## 🗂️ Project Structure

```
spyder-osint/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── modules/               # Core search modules
│   ├── person_search.py   # Person information gathering
│   ├── phone_search.py    # Phone number investigation
│   ├── email_search.py    # Email analysis
│   ├── social_media_search.py  # Social media discovery
│   └── image_search.py    # Image and photo search
├── utils/                 # Utility functions
│   ├── web_scraper.py     # Web scraping utilities
│   ├── display.py         # Result formatting
│   └── data_manager.py    # Data storage and export
├── core/                  # Core functionality
│   └── requester.py       # HTTP request handler
├── config/                # Configuration files
│   └── settings.py        # Application settings
└── results/               # Output directory (auto-created)
    └── *.json             # Investigation results
```

## ⚙️ Configuration

### Custom User Agents
Edit `utils/web_scraper.py` to add custom user agents:

```python
self.user_agents = [
    'Your Custom User Agent String',
    'Mozilla/5.0 (Custom Browser) ...',
]
```

### Search Delay Settings
Modify request delays in `utils/web_scraper.py`:

```python
time.sleep(random.uniform(0.5, delay))  # Adjust delay range
```

## 🔧 Advanced Usage

### Batch Processing
Create a script to process multiple targets:

```python
#!/usr/bin/env python3
from modules.person_search import PersonSearch

targets = [
    {"name": "John Smith", "location": "New York"},
    {"name": "Jane Doe", "location": "California"},
]

person_search = PersonSearch()
for target in targets:
    results = person_search.search(target["name"], target["location"])
    # Process results...
```

### Custom Search Engines
Add custom search engines in `modules/person_search.py`:

```python
self.search_engines = [
    "https://www.google.com/search?q=",
    "https://www.bing.com/search?q=",
    "https://your-custom-engine.com/search?q="
]
```

## 🚨 Legal and Ethical Guidelines

### ✅ Legitimate Uses
- Background verification for employment
- Reconnecting with lost contacts  
- Academic research with proper approval
- Cybersecurity investigations
- Due diligence for business purposes

### ❌ Prohibited Uses
- Stalking or harassment
- Identity theft
- Unauthorized surveillance  
- Doxxing or exposing private information
- Commercial data harvesting without permission

### 📜 Best Practices
1. **Always obtain proper authorization** before investigating individuals
2. **Respect privacy** and data protection laws (GDPR, CCPA, etc.)
3. **Use rate limiting** to avoid overwhelming target websites
4. **Document legitimate purpose** for your investigation
5. **Secure your results** and dispose of data appropriately

## 🐛 Troubleshooting

### Common Issues

**"Permission Denied" Error:**
```bash
chmod +x main.py
python3 main.py
```

**"Module Not Found" Error:**
```bash
pip install -r requirements.txt
```

**Rate Limiting Issues:**
- Increase delay settings in `web_scraper.py`
- Use VPN or proxy for IP rotation
- Reduce concurrent requests

**No Results Found:**
- Verify target name spelling
- Try variations of the name
- Check internet connection
- Some sites may block automated requests

### Debug Mode

Enable verbose output by modifying `main.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and open-source libraries
- Inspired by the OSINT community
- Uses publicly available data sources
- Respects robots.txt and rate limiting

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/spyder-osint/spyder-osint/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/spyder-osint/spyder-osint/discussions)
- 📧 **Contact**: [security@spyder-osint.com](mailto:security@spyder-osint.com)

---

**⚠️ Remember: With great power comes great responsibility. Use this tool ethically and legally.**

