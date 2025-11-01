import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from libs.config import info, run

def flash(function, links, thread_count):
    """Execute function on links using threading."""
    print(f"{info} Processing {len(links)} URLs with {thread_count} threads")
    
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = [executor.submit(function, link) for link in links]
        
        completed = 0
        for future in as_completed(futures):
            try:
                future.result()
                completed += 1
                if completed % 10 == 0:
                    print(f"{run} Processed {completed}/{len(links)} URLs")
            except Exception as e:
                print(f"Error processing URL: {e}")
                continue
