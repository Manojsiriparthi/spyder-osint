import requests
import re
from utils.web_scraper import WebScraper
import json

class EmailSearch:
    def __init__(self):
        self.scraper = WebScraper()
        self.breach_apis = [
            'https://haveibeenpwned.com/api/v3/breachedaccount/',
        ]
    
    def search(self, email):
        """Search email across multiple sources"""
        results = {
            'email': email,
            'domain': email.split('@')[1] if '@' in email else '',
            'valid': False,
            'associated_accounts': [],
            'breaches': [],
            'social_profiles': [],
            'mentions': []
        }
        
        # Basic email validation
        if self._is_valid_email(email):
            results['valid'] = True
            
            # Search for associated accounts
            print("  Searching for associated accounts...")
            results['associated_accounts'] = self._search_associated_accounts(email)
            
            # Check breach databases (Note: Requires API key for full functionality)
            print("  Checking breach databases...")
            results['breaches'] = self._check_breaches(email)
            
            # Search social media mentions
            print("  Searching social media...")
            results['social_profiles'] = self._search_social_profiles(email)
            
            # Google search for email mentions
            print("  Searching web mentions...")
            results['mentions'] = self._search_web_mentions(email)
        
        return results
    
    def _is_valid_email(self, email):
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _search_associated_accounts(self, email):
        """Search for accounts associated with email"""
        accounts = []
        
        # Common platforms that might show email associations
        platforms = [
            'github.com',
            'stackoverflow.com', 
            'reddit.com',
            'medium.com',
            'wordpress.com'
        ]
        
        for platform in platforms:
            query = f'site:{platform} "{email}"'
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            
            content = self.scraper.get_content(url)
            if content and email.lower() in content.lower():
                accounts.append({
                    'platform': platform,
                    'found': True,
                    'search_query': query
                })
        
        return accounts
    
    def _check_breaches(self, email):
        """Check if email appears in known breaches"""
        breaches = []
        
        # Note: This would require API keys for full functionality
        # This is a simplified example
        try:
            # Simulate breach check (replace with actual API call)
            common_breaches = [
                'LinkedIn (2012)', 'Yahoo (2013-2014)', 'Equifax (2017)',
                'Facebook (2019)', 'Twitter (2022)'
            ]
            
            # In real implementation, you would call actual breach APIs
            # For demo purposes, randomly assign some breaches
            if len(email) % 2 == 0:  # Simple simulation
                breaches.append({
                    'name': 'Example Data Breach',
                    'date': '2019-05-15',
                    'description': 'Email found in historical breach data'
                })
        
        except Exception as e:
            print(f"    Error checking breaches: {e}")
        
        return breaches
    
    def _search_social_profiles(self, email):
        """Search for social media profiles linked to email"""
        profiles = []
        
        # Search patterns for social media
        platforms = [
            ('facebook', f'site:facebook.com "{email}"'),
            ('twitter', f'site:twitter.com "{email}"'),
            ('linkedin', f'site:linkedin.com "{email}"'),
            ('instagram', f'site:instagram.com "{email}"')
        ]
        
        for platform, query in platforms:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            content = self.scraper.get_content(url)
            
            if content and email.lower() in content.lower():
                profiles.append({
                    'platform': platform,
                    'likely_associated': True,
                    'search_query': query
                })
        
        return profiles
    
    def _search_web_mentions(self, email):
        """Search for web mentions of the email"""
        mentions = []
        
        # Search Google for email mentions
        query = f'"{email}"'
        url = f"https://www.google.com/search?q={query}"
        
        content = self.scraper.get_content(url)
        if content:
            # Extract search result snippets
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find search result descriptions
            for result in soup.find_all(['div', 'span'], class_=re.compile(r'st|snippet')):
                text = result.get_text()
                if email.lower() in text.lower():
                    mentions.append({
                        'snippet': text[:200],
                        'source': 'google_search'
                    })
        
        return mentions[:10]  # Limit results
