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
    
    def _search_engine_query(self, query, engine_url):
        """Perform search engine query"""
        try:
            url = f"{engine_url}{query}"
            content = self.scraper.get_content(url)
            if content:
                soup = BeautifulSoup(content, 'html.parser')
                return self._parse_search_results(soup)
            return []
        except Exception as e:
            print(f"    Error searching {engine_url}: {str(e)}")
            return []

    def search(self, name: str, location: str = "") -> dict:
        """Search for person information"""
        results = {
            'name': name,
            'location': location,
            'addresses': [],
            'relatives': [],
            'occupations': [],
            'social_profiles': [],
            'phone_numbers': [],
            'emails': []
        }
        
        # Create search queries
        base_query = f'"{name}"'
        if location:
            location_query = f'"{name}" "{location}"'
        else:
            location_query = base_query
        
        # Search across multiple engines
        for engine_url in self.search_engines:
            try:
                print(f"  Searching {engine_url}...")
                search_results = self._search_engine_query(location_query, engine_url)
                self._extract_person_info(search_results, results)
            except Exception as e:
                print(f"    Error: {e}")
        
        return results
    
    def _parse_search_results(self, soup):
        """Parse search results from BeautifulSoup object"""
        results = []
        
        # Google results
        for result in soup.find_all('div', class_='g'):
            title_elem = result.find('h3')
            link_elem = result.find('a')
            snippet_elem = result.find('span')
            
            if title_elem and link_elem:
                results.append({
                    'title': title_elem.get_text(),
                    'url': link_elem.get('href', ''),
                    'snippet': snippet_elem.get_text() if snippet_elem else ''
                })
        
        return results
    
    def _extract_person_info(self, search_results, results):
        """Extract information from search results"""
        for result in search_results:
            title = result.get('title', '').lower()
            snippet = result.get('snippet', '').lower()
            
            # Look for address patterns
            if any(word in snippet for word in ['address', 'street', 'ave', 'road', 'blvd']):
                if results['location'].lower() in snippet:
                    results['addresses'].append(f"Address found in: {result['title']}")
            
            # Look for occupation information
            if any(word in snippet for word in ['works at', 'employed', 'company', 'job', 'career']):
                results['occupations'].append(f"Employment info: {result['title']}")
            
            # Look for social media profiles
            social_domains = ['facebook.com', 'linkedin.com', 'twitter.com', 'instagram.com']
            url = result.get('url', '')
            for domain in social_domains:
                if domain in url:
                    results['social_profiles'].append({
                        'platform': domain.replace('.com', ''),
                        'url': url,
                        'title': result.get('title', '')
                    })
