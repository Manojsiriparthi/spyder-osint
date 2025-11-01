import subprocess
import sys
from .config import info, good, bad

def updater():
    """Update the tool via git"""
    try:
        print(f'{info} Checking for updates...')
        
        # Try to pull latest changes
        result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
        
        if result.returncode == 0:
            if 'Already up to date' in result.stdout:
                print(f'{good} Already up to date')
            else:
                print(f'{good} Updated successfully')
                print(result.stdout)
        else:
            print(f'{bad} Update failed: {result.stderr}')
            
    except FileNotFoundError:
        print(f'{bad} Git not found. Please install git to use update functionality')
    except Exception as e:
        print(f'{bad} Update error: {e}')
