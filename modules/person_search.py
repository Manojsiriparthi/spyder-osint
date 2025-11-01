import requests
from bs4 import BeautifulSoup
import re
from utils.web_scraper import WebScraper

class PersonSearch:
    def __init__(self):
        self.scraper = WebScraper()
        self.search_engines = [
            "https://www.google.com/search?q=",
            "https://www.bing.com/search?q=",
            "https://duckduckgo.com/?q="
        ]
    
    def search(self, name, location=""):
        """Search for basic person information"""
        results = {
            'name': name,
            'location': location,
            'possible_addresses': [],
            'relatives': [],
            'age_estimates': [],
            'occupations': [],
            'education': [],
            'mentions': []
        }
        
        # Create search queries
        queries = [
            f'"{name}" address phone',
            f'"{name}" {location}' if location else f'"{name}"',
            f'"{name}" linkedin',
            f'"{name}" facebook',
            f'"{name}" work company',
            f'"{name}" family relatives'
        ]
        
        for query in queries:
            print(f"  Searching: {query}")
            search_results = self._search_engines(query)
            results['mentions'].extend(search_results)
        
        # Extract structured data
        self._extract_addresses(results)
        self._extract_relatives(results)
        self._extract_occupations(results)
        
        return results
    
    def _search_engines(self, query):
        """Search multiple search engines"""
        results = []
        
        for engine in self.search_engines:
            try:
                url = engine + query.replace(' ', '+')
                content = self.scraper.get_content(url)
                if content:
                    results.extend(self._parse_search_results(content))
            except Exception as e:
                print(f"    Error searching {engine}: {e}")
        
        return results
    
    def _parse_search_results(self, html):
        """Parse search engine results"""
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        # Find search result links and descriptions
        for result in soup.find_all(['div', 'li'], class_=re.compile(r'result|search')):
            link = result.find('a')
            desc = result.get_text()
            
            if link and desc:
                results.append({
                    'url': link.get('href', ''),
                    'description': desc.strip()[:200]
                })
        
        return results
    
    def _extract_addresses(self, results):
        """Extract possible addresses from mentions"""
        address_patterns = [
            r'\d+\s+\w+\s+(?:St|Street|Ave|Avenue|Rd|Road|Dr|Drive|Ln|Lane|Blvd|Boulevard)',
            r'\w+,\s*[A-Z]{2}\s+\d{5}',
        ]
        
        for mention in results['mentions']:
            text = mention.get('description', '')
            for pattern in address_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                results['possible_addresses'].extend(matches)
    
    def _extract_relatives(self, results):
        """Extract possible relatives"""
        relative_keywords = ['son', 'daughter', 'wife', 'husband', 'mother', 'father', 'brother', 'sister']
        
        for mention in results['mentions']:
            text = mention.get('description', '').lower()
            for keyword in relative_keywords:
                if keyword in text:
                    # Extract names near relative keywords
                    words = text.split()
                    for i, word in enumerate(words):
                        if keyword in word and i > 0:
                            possible_name = words[i-1] if i > 0 else ""
                            if possible_name and len(possible_name) > 2:
                                results['relatives'].append(f"{possible_name} ({keyword})")
    
    def _extract_occupations(self, results):
        """Extract occupation information"""
        job_keywords = ['works at', 'employed by', 'ceo', 'manager', 'director', 'engineer', 'doctor', 'lawyer']
        
        for mention in results['mentions']:
            text = mention.get('description', '').lower()
            for keyword in job_keywords:
                if keyword in text:
                    results['occupations'].append(text[:100])
