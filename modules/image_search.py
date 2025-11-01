import requests
from bs4 import BeautifulSoup
from utils.web_scraper import WebScraper
import json

class ImageSearch:
    def __init__(self):
        self.scraper = WebScraper()
    
    def search_person_images(self, name):
        """Search for images of a person across multiple sources"""
        results = {
            'google_images': [],
            'bing_images': [],
            'social_media_photos': [],
            'profile_pictures': []
        }
        
        # Google Images
        print("  Searching Google Images...")
        results['google_images'] = self._google_image_search(name)
        
        # Bing Images
        print("  Searching Bing Images...")
        results['bing_images'] = self._bing_image_search(name)
        
        # Social media profile pictures
        print("  Searching for profile pictures...")
        results['profile_pictures'] = self._search_profile_pictures(name)
        
        return results
    
    def _google_image_search(self, query):
        """Search Google Images"""
        url = f"https://www.google.com/search?tbm=isch&q={query.replace(' ', '+')}"
        content = self.scraper.get_content(url)
        images = []
        
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find image elements
            img_tags = soup.find_all('img')
            for img in img_tags:
                src = img.get('src') or img.get('data-src')
                if src and 'http' in src:
                    images.append({
                        'url': src,
                        'alt': img.get('alt', ''),
                        'title': img.get('title', ''),
                        'source': 'google'
                    })
        
        return images[:20]  # Limit results
    
    def _bing_image_search(self, query):
        """Search Bing Images"""
        url = f"https://www.bing.com/images/search?q={query.replace(' ', '+')}"
        content = self.scraper.get_content(url)
        images = []
        
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            
            # Bing uses different structure
            for img in soup.find_all('img', {'class': 'mimg'}):
                src = img.get('src')
                if src:
                    images.append({
                        'url': src,
                        'alt': img.get('alt', ''),
                        'source': 'bing'
                    })
        
        return images[:20]
    
    def _search_profile_pictures(self, name):
        """Search for profile pictures on social platforms"""
        results = []
        
        # Search for common profile picture patterns
        platforms = [
            ('facebook', f"site:facebook.com {name} profile picture"),
            ('linkedin', f"site:linkedin.com {name} profile"),
            ('twitter', f"site:twitter.com {name} profile"),
            ('instagram', f"site:instagram.com {name}")
        ]
        
        for platform, query in platforms:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            content = self.scraper.get_content(url)
            
            if content:
                # Look for profile picture URLs in search results
                profile_pics = self._extract_profile_pics(content, platform)
                results.extend(profile_pics)
        
        return results
    
    def _extract_profile_pics(self, html, platform):
        """Extract profile picture URLs from search results"""
        pics = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Look for images in search results
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and platform in src:
                pics.append({
                    'url': src,
                    'platform': platform,
                    'type': 'profile_picture'
                })
        
        return pics[:5]  # Limit per platform
