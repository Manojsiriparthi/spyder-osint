import threading
from queue import Queue
from .config import info, bad

def flash(function, urls, thread_count):
    """Execute function on URLs using threading"""
    
    def worker():
        while True:
            url = url_queue.get()
            if url is None:
                break
            try:
                function(url)
            except Exception as e:
                print(f"Error processing {url}: {e}")
            finally:
                url_queue.task_done()
    
    url_queue = Queue()
    
    # Start threads
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        threads.append(t)
    
    # Add URLs to queue
    for url in urls:
        url_queue.put(url)
    
    # Wait for completion
    url_queue.join()
    
    # Stop threads
    for _ in range(thread_count):
        url_queue.put(None)
    
    for t in threads:
        t.join()
