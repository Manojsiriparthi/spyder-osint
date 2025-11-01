import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from .config import info, bad

def flash(function, links, thread_count):
    """Execute function on links using thread pool"""
    
    if not links:
        return
    
    links_list = list(links) if not isinstance(links, list) else links
    
    try:
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            # Submit all tasks
            futures = {executor.submit(function, link): link for link in links_list}
            
            # Process completed tasks
            for future in as_completed(futures):
                link = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f'{bad} Error processing {link}: {str(e)}')
                    
    except KeyboardInterrupt:
        print(f'\n{info} Interrupted by user')
        raise
    except Exception as e:
        print(f'{bad} Threading error: {str(e)}')
