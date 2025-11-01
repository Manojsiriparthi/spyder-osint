#!/usr/bin/env python3
import asyncio
from modules.person_search import PersonSearch
from modules.phone_search import PhoneSearch
from modules.email_search import EmailSearch
from modules.social_media_search import SocialMediaSearch
from modules.image_search import ImageSearch
from utils.display import display_results, print_banner
from utils.data_manager import DataManager

def main():
    print_banner()
    
    print("=" * 60)
    print("SPYDER OSINT - Person Intelligence Gathering")
    print("=" * 60)
    
    # Get search parameters
    target_name = input("Enter full name: ").strip()
    phone_number = input("Enter phone number (optional): ").strip()
    email = input("Enter email (optional): ").strip()
    location = input("Enter location/city (optional): ").strip()
    
    if not target_name:
        print("Name is required!")
        return
    
    # Initialize search modules
    person_search = PersonSearch()
    phone_search = PhoneSearch()
    email_search = EmailSearch()
    social_search = SocialMediaSearch()
    image_search = ImageSearch()
    data_manager = DataManager()
    
    print("\n[+] Starting OSINT investigation...")
    
    # Collect all data
    results = {}
    
    # Basic person search
    print("[+] Searching basic information...")
    results['person'] = person_search.search(target_name, location)
    
    # Phone number search
    if phone_number:
        print("[+] Searching phone number...")
        results['phone'] = phone_search.search(phone_number)
    
    # Email search
    if email:
        print("[+] Searching email...")
        results['email'] = email_search.search(email)
    
    # Social media search
    print("[+] Searching social media...")
    results['social'] = social_search.search_all_platforms(target_name, location)
    
    # Image search
    print("[+] Searching for photos...")
    results['images'] = image_search.search_person_images(target_name)
    
    # Save and display results
    data_manager.save_results(target_name, results)
    display_results(results)

if __name__ == "__main__":
    main()
