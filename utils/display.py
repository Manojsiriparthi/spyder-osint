import json
from datetime import datetime

def print_banner():
    """Print application banner"""
    banner = """
    ███████╗██████╗ ██╗   ██╗██████╗ ███████╗██████╗ 
    ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
    ███████╗██████╔╝ ╚████╔╝ ██║  ██║█████╗  ██████╔╝
    ╚════██║██╔═══╝   ╚██╔╝  ██║  ██║██╔══╝  ██╔══██╗
    ███████║██║        ██║   ██████╔╝███████╗██║  ██║
    ╚══════╝╚═╝        ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
                    
                    OSINT Intelligence Gathering
                    Version 2.0 | github.com/spyder-osint
    """
    print(banner)

def display_results(results):
    """Display formatted results"""
    print("\n" + "="*80)
    print("INVESTIGATION RESULTS")
    print("="*80)
    
    # Person Information
    if 'person' in results:
        display_person_info(results['person'])
    
    # Phone Information
    if 'phone' in results:
        display_phone_info(results['phone'])
    
    # Email Information
    if 'email' in results:
        display_email_info(results['email'])
    
    # Social Media
    if 'social' in results:
        display_social_media(results['social'])
    
    # Images
    if 'images' in results:
        display_images(results['images'])

def display_person_info(person_data):
    """Display person information"""
    print("\n📋 PERSONAL INFORMATION")
    print("-" * 40)
    print(f"Name: {person_data.get('name', 'N/A')}")
    print(f"Location: {person_data.get('location', 'N/A')}")
    
    if person_data.get('possible_addresses'):
        print("\n🏠 Possible Addresses:")
        for addr in person_data['possible_addresses'][:5]:
            print(f"  • {addr}")
    
    if person_data.get('relatives'):
        print("\n👨‍👩‍👧‍👦 Possible Relatives:")
        for rel in person_data['relatives'][:5]:
            print(f"  • {rel}")
    
    if person_data.get('occupations'):
        print("\n💼 Occupation Information:")
        for occ in person_data['occupations'][:3]:
            print(f"  • {occ}")

def display_phone_info(phone_data):
    """Display phone information"""
    print("\n📞 PHONE INFORMATION")
    print("-" * 40)
    print(f"Number: {phone_data.get('phone_number', 'N/A')}")
    print(f"Location: {phone_data.get('location', 'N/A')}")
    print(f"Carrier: {phone_data.get('carrier', 'N/A')}")
    
    if phone_data.get('associated_names'):
        print("\n👤 Associated Names:")
        for name in phone_data['associated_names'][:5]:
            print(f"  • {name}")

def display_social_media(social_data):
    """Display social media findings"""
    print("\n📱 SOCIAL MEDIA ACCOUNTS")
    print("-" * 40)
    
    for platform, accounts in social_data.items():
        if accounts:
            print(f"\n{platform.upper()}:")
            for account in accounts[:3]:
                if isinstance(account, dict):
                    name = account.get('name') or account.get('username', 'N/A')
                    print(f"  • {name}")
                    if account.get('url'):
                        print(f"    URL: {account['url']}")

def display_images(image_data):
    """Display image findings"""
    print("\n📸 FOUND IMAGES")
    print("-" * 40)
    
    total_images = 0
    for source, images in image_data.items():
        if images:
            print(f"\n{source.replace('_', ' ').title()}: {len(images)} images")
            total_images += len(images)
    
    print(f"\nTotal images found: {total_images}")
    print("Note: Image URLs saved to results file")

def save_results_json(name, results, filename=None):
    """Save results to JSON file"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results_{name.replace(' ', '_')}_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {filename}")
