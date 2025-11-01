import json
from datetime import datetime
from colorama import Fore, Back, Style, init
import sys

# Initialize colorama
init(autoreset=True)

class Display:
    def __init__(self):
        self.colors = {
            'header': Fore.CYAN + Style.BRIGHT,
            'success': Fore.GREEN + Style.BRIGHT,
            'warning': Fore.YELLOW + Style.BRIGHT,
            'error': Fore.RED + Style.BRIGHT,
            'info': Fore.BLUE + Style.BRIGHT,
            'reset': Style.RESET_ALL
        }
    
    def print_banner(self):
        """Print application banner"""
        banner = f"""
{self.colors['header']}
    ███████╗██████╗ ██╗   ██╗██████╗ ███████╗██████╗ 
    ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
    ███████╗██████╔╝ ╚████╔╝ ██║  ██║█████╗  ██████╔╝
    ╚════██║██╔═══╝   ╚██╔╝  ██║  ██║██╔══╝  ██╔══██╗
    ███████║██║        ██║   ██████╔╝███████╗██║  ██║
    ╚══════╝╚═╝        ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
                    
                    OSINT Intelligence Gathering
                    Version 2.0 | github.com/spyder-osint
{self.colors['reset']}
============================================================
SPYDER OSINT - Person Intelligence Gathering
============================================================
        """
        print(banner)
    
    def print_header(self, text: str):
        """Print section header"""
        print(f"\n{self.colors['header']}{'='*60}")
        print(f"{text}")
        print(f"{'='*60}{self.colors['reset']}")
    
    def print_success(self, text: str):
        """Print success message"""
        print(f"{self.colors['success']}[+] {text}{self.colors['reset']}")
    
    def print_error(self, text: str):
        """Print error message"""
        print(f"{self.colors['error']}[-] {text}{self.colors['reset']}")
    
    def print_warning(self, text: str):
        """Print warning message"""
        print(f"{self.colors['warning']}[!] {text}{self.colors['reset']}")
    
    def print_info(self, text: str):
        """Print info message"""
        print(f"{self.colors['info']}[*] {text}{self.colors['reset']}")
    
    def print_results(self, results: dict):
        """Print formatted investigation results"""
        if not results:
            self.print_warning("No results found")
            return
        
        # Personal Information
        if 'person' in results:
            self.print_header("📋 PERSONAL INFORMATION")
            person = results['person']
            print(f"Name: {person.get('name', 'N/A')}")
            print(f"Location: {person.get('location', 'N/A')}")
            
            if person.get('addresses'):
                print("\n🏠 Possible Addresses:")
                for addr in person['addresses']:
                    print(f"  • {addr}")
            
            if person.get('relatives'):
                print("\n👨‍👩‍👧‍👦 Possible Relatives:")
                for rel in person['relatives']:
                    print(f"  • {rel}")
        
        # Social Media
        if 'social' in results:
            self.print_header("📱 SOCIAL MEDIA ACCOUNTS")
            social = results['social']
            
            for platform, accounts in social.items():
                if accounts:
                    print(f"\n{platform.upper()}:")
                    for account in accounts:
                        print(f"  • {account.get('name', 'N/A')}")
                        if account.get('url'):
                            print(f"    URL: {account['url']}")
        
        # Images
        if 'images' in results:
            total_images = sum(len(imgs) for imgs in results['images'].values())
            self.print_header("📸 IMAGES FOUND")
            print(f"Total images found: {total_images}")
            for source, images in results['images'].items():
                print(f"{source.replace('_', ' ').title()}: {len(images)} images")

# Global functions for compatibility with main.py imports
def print_banner():
    """Print application banner - global function"""
    display = Display()
    display.print_banner()

def display_results(results):
    """Display formatted results - global function"""
    display = Display()
    display.print_results(results)

def save_results_json(name, results, filename=None):
    """Save results to JSON file"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results_{name.replace(' ', '_')}_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {filename}")
