
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import random

# User agent to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Target categories
TARGET_CATEGORIES = [
    'Facebook Ads Advertiser',
    'Google Ads Advertiser', 
    'TikTok Ads Advertiser',
    'Cross-border E-commerce Seller',
    'Advertising Agency'
]

# Public sources to scrape
SOURCES = [
    'https://www.ecommercefuel.com/top-ecommerce-stores/',
    'https://www.shopify.com/examples',
    'https://clutch.co/advertising/agencies/tiktok'
]

def extract_emails(text):
    """Extract public email addresses from text"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return list(set(re.findall(email_pattern, text)))

def extract_websites(text):
    """Extract website urls from text"""
    website_pattern = r'https?://(?:www\.)?[a-zA-Z0-9./-]+'
    return list(set(re.findall(website_pattern, text)))

def scrape_ecommercefuel():
    """Scrape top ecommerce stores from ecommercefuel"""
    customers = []
    try:
        response = requests.get(SOURCES[0], headers=HEADERS, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            store_cards = soup.select('.store-card')[:50]  # Get top 50 stores
            
            for card in store_cards:
                store_name = card.select_one('.store-name').text.strip() if card.select_one('.store-name') else ''
                store_url = card.select_one('a')['href'] if card.select_one('a') else ''
                description = card.select_one('.store-description').text.strip() if card.select_one('.store-description') else ''
                
                # Check if store is target customer
                is_target = any(keyword.lower() in description.lower() for keyword in ['facebook ads', 'google ads', 'tiktok ads', 'dropshipping', 'ecommerce'])
                if is_target:
                    customer = {
                        'name': store_name,
                        'category': 'Cross-border E-commerce Seller',
                        'website': store_url,
                        'description': description,
                        'email': '',
                        'source': 'ecommercefuel.com'
                    }
                    customers.append(customer)
            time.sleep(random.uniform(1,3))
    except Exception as e:
        print(f"Error scraping ecommercefuel: {str(e)}")
    return customers

def scrape_shopify_examples():
    """Scrape Shopify example stores"""
    customers = []
    try:
        response = requests.get(SOURCES[1], headers=HEADERS, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            example_cards = soup.select('.example-card')[:50]
            
            for card in example_cards:
                store_name = card.select_one('.example-card__title').text.strip() if card.select_one('.example-card__title') else ''
                store_url = card.select_one('a')['href'] if card.select_one('a') else ''
                industry = card.select_one('.example-card__industry').text.strip() if card.select_one('.example-card__industry') else ''
                
                customer = {
                    'name': store_name,
                    'category': 'Cross-border E-commerce Seller',
                    'website': store_url,
                    'description': f"Industry: {industry}, Successful Shopify store using digital advertising",
                    'email': '',
                    'source': 'shopify.com/examples'
                }
                customers.append(customer)
            time.sleep(random.uniform(1,3))
    except Exception as e:
        print(f"Error scraping shopify examples: {str(e)}")
    return customers

def scrape_clutch_agencies():
    """Scrape TikTok/Google/Facebook ad agencies from clutch.co"""
    customers = []
    try:
        response = requests.get(SOURCES[2], headers=HEADERS, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            agency_cards = soup.select('.company_info')[:50]
            
            for card in agency_cards:
                agency_name = card.select_one('.company_name a').text.strip() if card.select_one('.company_name a') else ''
                website = card.select_one('.website-link a')['href'] if card.select_one('.website-link a') else ''
                description = card.select_one('.company_tagline').text.strip() if card.select_one('.company_tagline') else ''
                location = card.select_one('.location').text.strip() if card.select_one('.location') else ''
                
                # Check ad types
                ad_types = []
                if 'facebook' in description.lower():
                    ad_types.append('Facebook Ads')
                if 'google' in description.lower():
                    ad_types.append('Google Ads')
                if 'tiktok' in description.lower():
                    ad_types.append('TikTok Ads')
                
                customer = {
                    'name': agency_name,
                    'category': 'Advertising Agency' + (f' (Specialties: {", ".join(ad_types)})' if ad_types else ''),
                    'website': website,
                    'description': f"{description} | Location: {location}",
                    'email': '',
                    'source': 'clutch.co'
                }
                customers.append(customer)
            time.sleep(random.uniform(1,3))
    except Exception as e:
        print(f"Error scraping clutch agencies: {str(e)}")
    return customers

def main():
    all_customers = []
    
    print("Scraping ecommerce fuel stores...")
    all_customers.extend(scrape_ecommercefuel())
    
    print("Scraping Shopify example stores...")
    all_customers.extend(scrape_shopify_examples())
    
    print("Scraping clutch ad agencies...")
    all_customers.extend(scrape_clutch_agencies())
    
    # Deduplicate by website
    seen_websites = set()
    unique_customers = []
    for customer in all_customers:
        if customer['website'] not in seen_websites and customer['website']:
            seen_websites.add(customer['website'])
            unique_customers.append(customer)
    
    from tg_monitor_kit.config import get_web_output_dir

    df = pd.DataFrame(unique_customers)
    out_dir = get_web_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = str(out_dir / "public-target-customers.xlsx")
    df.to_excel(output_path, index=False)
    
    print(f"Successfully saved {len(unique_customers)} target customers to {output_path}")
    return len(unique_customers)

if __name__ == '__main__':
    count = main()
