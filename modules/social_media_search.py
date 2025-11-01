import requests
from bs4 import BeautifulSoup
from utils.web_scraper import WebScraper
import json

class SocialMediaSearch:
    def __init__(self):
        self.scraper = WebScraper()
        self.platforms = {
            'facebook': 'https://www.facebook.com/search/people/?q=',
            'twitter': 'https://twitter.com/search?q=',
            'instagram': 'https://www.instagram.com/',
            'linkedin': 'https://www.linkedin.com/search/results/people/?keywords=',
            'tiktok': 'https://www.tiktok.com/search/user?q=',
            'youtube': 'https://www.youtube.com/results?search_query='
        }
    
    def search_all_platforms(self, name, location=""):
        """Search across all social media platforms"""
        results = {}
        
        for platform, base_url in self.platforms.items():
            print(f"  Searching {platform}...")
            try:
                platform_results = self._search_platform(platform, name, location, base_url)
                results[platform] = platform_results
            except Exception as e:
                print(f"    Error searching {platform}: {e}")
                results[platform] = []
        
        return results
    
    def _search_platform(self, platform, name, location, base_url):
        """Search specific platform"""
        query = f"{name} {location}".strip()
        url = base_url + query.replace(' ', '+')
        
        content = self.scraper.get_content(url)
        if not content:
            return []
        
        if platform == 'facebook':
            return self._parse_facebook(content)
        elif platform == 'twitter':
            return self._parse_twitter(content)
        elif platform == 'linkedin':
            return self._parse_linkedin(content)
        elif platform == 'instagram':
            return self._parse_instagram(content)
        else:
            return self._parse_generic(content)
    
    def _parse_facebook(self, html):
        """Parse Facebook search results"""
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Look for profile elements
        for profile in soup.find_all('div', {'data-testid': re.compile(r'search_result')}):
            name = profile.find(['h3', 'h4'])
            link = profile.find('a')
            
            if name and link:
                results.append({
                    'name': name.get_text().strip(),
                    'url': link.get('href'),
                    'platform': 'facebook'
                })
        
        return results
    
    def _parse_twitter(self, html):
        """Parse Twitter search results"""
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        
        for tweet in soup.find_all('div', {'data-testid': 'cellInnerDiv'}):
            username = tweet.find('span', string=re.compile(r'@\w+'))
            display_name = tweet.find('div', {'data-testid': 'User-Names'})
            
            if username and display_name:
                results.append({
                    'username': username.get_text(),
                    'display_name': display_name.get_text(),
                    'platform': 'twitter'
                })
        
        return results
    
    def _parse_linkedin(self, html):
        """Parse LinkedIn search results"""
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        
        for result in soup.find_all('li', class_=re.compile(r'search-result')):
            name = result.find('span', {'aria-hidden': 'true'})
            title = result.find('p', class_=re.compile(r'subline'))
            link = result.find('a')
            
            if name and link:
                results.append({
                    'name': name.get_text().strip(),
                    'title': title.get_text().strip() if title else '',
                    'url': link.get('href'),
                    'platform': 'linkedin'
                })
        
        return results
    
    def _parse_instagram(self, html):
        """Parse Instagram search results"""
        results = []
        # Instagram requires special handling due to JavaScript
        # This is a simplified version
        soup = BeautifulSoup(html, 'html.parser')
        
        # Look for JSON data in script tags
        for script in soup.find_all('script'):
            if 'window._sharedData' in script.get_text():
                try:
                    json_text = script.get_text().split('window._sharedData = ')[1].split(';</script>')[0]
                    data = json.loads(json_text)
                    # Extract user data from JSON
                    # This would need more specific parsing based on Instagram's structure
                except:
                    pass
        
        return results
    
    def _parse_generic(self, html):
        """Generic parser for other platforms"""
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Look for profile-like elements
        for link in soup.find_all('a', href=True):
            text = link.get_text().strip()
            if len(text) > 3 and len(text) < 50:
                results.append({
                    'text': text,
                    'url': link['href']
                })
        
        return results[:10]  # Limit results
