import requests
import re
from utils.web_scraper import WebScraper
from bs4 import BeautifulSoup

class PhoneSearch:
    def __init__(self):
        self.scraper = WebScraper()
        self.lookup_sites = [
            'https://www.truecaller.com/search/us/',
            'https://www.whitepages.com/phone/',
            'https://www.spokeo.com/phone-search/',
        ]
    
    def search(self, phone_number):
        """Search phone number across multiple sources"""
        # Clean phone number
        cleaned_number = re.sub(r'[^\d]', '', phone_number)
        
        results = {
            'phone_number': phone_number,
            'cleaned_number': cleaned_number,
            'carrier': '',
            'location': '',
            'type': '',
            'associated_names': [],
            'associated_addresses': [],
            'social_media_links': [],
            'reports': []
        }
        
        # Get carrier and location info
        results.update(self._get_carrier_info(cleaned_number))
        
        # Search lookup sites
        for site in self.lookup_sites:
            try:
                print(f"  Checking {site}...")
                site_results = self._search_lookup_site(site, cleaned_number)
                self._merge_results(results, site_results)
            except Exception as e:
                print(f"    Error: {e}")
        
        # Search Google for phone number
        google_results = self._google_search(cleaned_number)
        results['reports'].extend(google_results.get('search_results', []))
        
        return results
    
    def _get_carrier_info(self, number):
        """Get carrier and location information"""
        info = {}
        
        if len(number) == 10:
            area_code = number[:3]
            
            # Basic area code to region mapping
            area_codes = {
                '212': 'New York, NY', '213': 'Los Angeles, CA', '214': 'Dallas, TX',
                '215': 'Philadelphia, PA', '216': 'Cleveland, OH', '217': 'Illinois',
                # Add more area codes as needed
            }
            
            info['location'] = area_codes.get(area_code, f'Area Code: {area_code}')
        
        return info
    
    def _search_lookup_site(self, site_url, number):
        """Search phone lookup site"""
        url = site_url + number
        content = self.scraper.get_content(url)
        
        results = {
            'names': [],
            'addresses': [],
            'carriers': []
        }
        
        if content:
            # Extract names (simplified parsing)
            name_patterns = [
                r'<h1[^>]*>([^<]+)</h1>',
                r'<span class="name[^"]*">([^<]+)</span>',
                r'"name":\s*"([^"]+)"'
            ]
            
            for pattern in name_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                results['names'].extend(matches)
            
            # Extract addresses
            address_patterns = [
                r'\d+\s+[A-Za-z\s]+(?:St|Street|Ave|Avenue|Rd|Road|Dr|Drive)',
                r'[A-Za-z\s]+,\s*[A-Z]{2}\s+\d{5}'
            ]
            
            for pattern in address_patterns:
                matches = re.findall(pattern, content)
                results['addresses'].extend(matches)
        
        return results
    
    def _google_search(self, phone_number):
        """Search for phone number information on Google"""
        try:
            query = f'"{phone_number}" OR "{phone_number.replace("-", "")}" OR "{phone_number.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")}"'
            url = f"https://www.google.com/search?q={query}"
            
            content = self.scraper.get_content(url)
            if not content:
                return {}
                
            soup = BeautifulSoup(content, 'html.parser')
            
            results = {
                'search_results': [],
                'associated_names': [],
                'addresses': []
            }
            
            # Extract search results
            for result in soup.find_all('div', class_='g')[:10]:
                title_elem = result.find('h3')
                link_elem = result.find('a')
                snippet_elem = result.find('span')
                
                if title_elem and link_elem:
                    results['search_results'].append({
                        'title': title_elem.get_text(),
                        'url': link_elem.get('href'),
                        'snippet': snippet_elem.get_text() if snippet_elem else ''
                    })
            
            return results
            
        except Exception as e:
            print(f"Error in Google search: {e}")
            return {}
    
    def _merge_results(self, main_results, new_results):
        """Merge new results into main results"""
        main_results['associated_names'].extend(new_results.get('names', []))
        main_results['associated_addresses'].extend(new_results.get('addresses', []))
        
        # Remove duplicates
        main_results['associated_names'] = list(set(main_results['associated_names']))
        main_results['associated_addresses'] = list(set(main_results['associated_addresses']))
