import requests
from bs4 import BeautifulSoup
import random
import time
from urllib.parse import urljoin, urlparse
from fake_useragent import UserAgent

class WebScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def get_random_headers(self):
        """Get random headers for requests"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def get_page(self, url: str, headers=None, delay: float = 1.0):
        """Get page content as text"""
        try:
            time.sleep(random.uniform(0.5, delay))
            
            if headers is None:
                headers = self.get_random_headers()
            
            response = self.session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            return response.text
            
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def get_content(self, url, headers=None):
        """Get content from URL - alias for get_page method"""
        return self.get_page(url, headers)
    
    def fetch_page(self, url: str, delay: float = 1.0) -> BeautifulSoup:
        """Fetch and parse a web page"""
        try:
            content = self.get_page(url, delay=delay)
            if content:
                return BeautifulSoup(content, 'html.parser')
            return None
            
        except Exception as e:
            print(f"Error parsing {url}: {e}")
            return None
    
    def search_google(self, query: str, num_results: int = 10) -> list:
        """Search Google and return results"""
        results = []
        try:
            search_url = f"https://www.google.com/search?q={query}&num={num_results}"
            soup = self.fetch_page(search_url)
            
            if soup:
                # Parse Google search results
                search_results = soup.find_all('div', class_='g')
                for result in search_results[:num_results]:
                    title_elem = result.find('h3')
                    link_elem = result.find('a')
                    snippet_elem = result.find('span', class_='st')
                    
                    if title_elem and link_elem:
                        results.append({
                            'title': title_elem.get_text(),
                            'url': link_elem.get('href'),
                            'snippet': snippet_elem.get_text() if snippet_elem else ''
                        })
            
        except Exception as e:
            print(f"Error searching Google: {e}")
        
        return results
    
    def extract_links(self, soup: BeautifulSoup, base_url: str = None) -> list:
        """Extract all links from a page"""
        links = []
        if soup:
            for link in soup.find_all('a', href=True):
                url = link['href']
                if base_url:
                    url = urljoin(base_url, url)
                links.append(url)
        return links
    
    def extract_images(self, soup: BeautifulSoup, base_url: str = None) -> list:
        """Extract all images from a page"""
        images = []
        if soup:
            for img in soup.find_all('img', src=True):
                url = img['src']
                if base_url:
                    url = urljoin(base_url, url)
                images.append({
                    'url': url,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                })
        return images
