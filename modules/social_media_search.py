import re
import requests
from bs4 import BeautifulSoup
from utils.web_scraper import WebScraper
import json
import urllib.parse

class SocialMediaSearch:
    def __init__(self):
        self.scraper = WebScraper()
        self.platforms = {
            'facebook': 'site:facebook.com',
            'twitter': 'site:twitter.com',
            'linkedin': 'site:linkedin.com',
            'instagram': 'site:instagram.com'
        }
    
    def search_all_platforms(self, name: str) -> dict:
        """Search all social media platforms"""
        results = {}
        
        for platform, site_query in self.platforms.items():
            results[platform] = self.search_platform(name, platform, site_query)
        
        return results
    
    def search_platform(self, name: str, platform: str, site_query: str) -> list:
        """Search specific social media platform"""
        accounts = []
        
        try:
            query = f'{site_query} "{name}"'
            search_results = self.scraper.search_google(query, num_results=5)
            
            for result in search_results:
                if platform in result.get('url', '').lower():
                    accounts.append({
                        'name': result.get('title', ''),
                        'url': result.get('url', ''),
                        'platform': platform,
                        'snippet': result.get('snippet', '')
                    })
        
        except Exception as e:
            print(f"Error searching {platform}: {e}")
        
        return accounts
