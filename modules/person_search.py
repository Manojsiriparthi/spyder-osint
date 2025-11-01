import requests
from bs4 import BeautifulSoup
import re
from utils.web_scraper import WebScraper
import urllib.parse

class PersonSearch:
    def __init__(self):
        self.scraper = WebScraper()
        self.search_engines = [
            "https://www.google.com/search?q=",
            "https://www.bing.com/search?q=",
            "https://duckduckgo.com/?q="
        ]
    
    def search(self, name: str, location: str = "") -> dict:
        """Search for person information"""
        results = {
            'name': name,
            'location': location,
            'addresses': [],
            'relatives': [],
            'occupations': []
        }
        
        # Create search query
        query = f'"{name}"'
        if location:
            query += f' "{location}"'
        
        # Search for basic information
        search_results = self.scraper.search_google(query, num_results=10)
        
        # Extract information from search results
        for result in search_results:
            title = result.get('title', '').lower()
            snippet = result.get('snippet', '').lower()
            
            # Look for address patterns
            if any(word in snippet for word in ['address', 'street', 'ave', 'road', 'blvd']):
                # Extract potential addresses (simplified)
                if location.lower() in snippet:
                    results['addresses'].append(f"Address found in: {result['title']}")
            
            # Look for occupation information
            if any(word in snippet for word in ['works at', 'employed', 'company', 'job', 'career']):
                results['occupations'].append(f"Employment info: {result['title']}")
        
        return results
