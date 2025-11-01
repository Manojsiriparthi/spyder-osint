import re
import threading
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.requester import requester
from core.regex import rintels, rendpoint, rhref, rscript, rentropy
from core.utils import is_link, entropy, regxy
from libs.config import info, good, bad, run

def flash(main_url, cook, headers, timeout, host, proxies, user_agents, 
          failed, processed, internal, external, files, intel, robots, 
          custom, scripts, level, delay, regex_pattern, exclude_pattern):
    """Main crawling function that processes URLs and extracts data"""
    
    all_crawled = set()
    current_level_urls = {main_url}
    
    for current_level in range(level + 1):
        if not current_level_urls:
            break
            
        print(f"{info} Crawling level {current_level} ({len(current_level_urls)} URLs)")
        next_level_urls = set()
        
        for url in current_level_urls:
            if url in processed:
                continue
                
            response_text = requester(url, main_url, delay, cook, headers, 
                                    timeout, host, proxies, user_agents, 
                                    failed, processed)
            
            if not response_text:
                continue
                
            all_crawled.add(url)
            
            # Extract links
            extracted_links = rhref(response_text, url, main_url, host)
            for link in extracted_links:
                if exclude_pattern and re.search(exclude_pattern, link):
                    continue
                    
                if is_link(link, main_url):
                    if urlparse(link).netloc == host:
                        internal.add(link)
                        if current_level < level:
                            next_level_urls.add(link)
                    else:
                        external.add(link)
            
            # Extract files
            file_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', 
                             '.ppt', '.pptx', '.txt', '.zip', '.rar', '.7z']
            for ext in file_extensions:
                pattern = rf'href=["\']([^"\']*\{ext})["\']'
                matches = re.findall(pattern, response_text, re.IGNORECASE)
                for match in matches:
                    full_url = urljoin(url, match)
                    files.add(full_url)
            
            # Extract intelligence data
            intel_data = rintels(response_text, main_url)
            intel.update(intel_data)
            
            # Extract endpoints
            endpoints = rendpoint(response_text, main_url)
            for endpoint in endpoints:
                custom.add(endpoint)
            
            # Extract scripts
            script_data = rscript(response_text, url)
            scripts.update(script_data)
            
            # Custom regex matching
            if regex_pattern:
                custom_matches = regxy(response_text, regex_pattern)
                for match in custom_matches:
                    custom.add(match)
            
            # Check entropy for secrets
            high_entropy_strings = rentropy(response_text)
            intel.update(high_entropy_strings)
        
        current_level_urls = next_level_urls
    
    print(f"{good} Crawling completed. Processed {len(all_crawled)} URLs")
