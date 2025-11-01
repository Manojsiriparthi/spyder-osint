import re
import requests
from bs4 import BeautifulSoup
from utils.web_scraper import WebScraper
import json

class SocialMediaSearch:
    def __init__(self):
        self.scraper = WebScraper()
        self.platforms = {
            'facebook': 'https://www.google.com/search?q=site:facebook.com+',
            'twitter': 'https://www.google.com/search?q=site:twitter.com+',
            'instagram': 'https://www.google.com/search?q=site:instagram.com+',
            'linkedin': 'https://www.google.com/search?q=site:linkedin.com+',
            'tiktok': 'https://www.google.com/search?q=site:tiktok.com+',
            'youtube': 'https://www.google.com/search?q=site:youtube.com+'
        }
    
    def search_all_platforms(self, name, location=""):
        """Search across all social media platforms using Google site search"""
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
        """Search specific platform via Google"""
        query = f'"{name}" {location}'.strip()
        url = base_url + query.replace(' ', '+')
        
        content = self.scraper.get_content(url)
        if not content:
            return []
        
        return self._parse_google_results(content, platform)
    
    def _parse_google_results(self, html, platform):
        """Parse Google search results for social media profiles"""
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Look for search result links
        for result_div in soup.find_all('div', class_=re.compile(r'g\b')):
            link_element = result_div.find('a', href=True)
            title_element = result_div.find('h3')
            
            if link_element and title_element and platform in link_element['href']:
                results.append({
                    'name': title_element.get_text().strip(),
                    'url': link_element['href'],
                    'platform': platform
                })
        
        return results[:5]  # Limit results per platform
