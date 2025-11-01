import threading
from concurrent.futures import ThreadPoolExecutor

def flash(function, links, thread_count):
    """Execute function on links using threading."""
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        executor.map(function, links)
