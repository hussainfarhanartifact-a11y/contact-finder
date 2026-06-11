# ============================================================
#  Business Contact Finder — by Hussain Farhan
#  Scrapes author/business profiles from quotes.toscrape.com/author
#  In real use: swap target URL for any business directory
#  Saves results to contacts.csv
# ============================================================

import requests
from bs4 import BeautifulSoup
import csv
from datetime import date
import time

BASE_URL = "https://quotes.toscrape.com"

def get_page(url):
    """Fetch a page and return a BeautifulSoup object."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, "html.parser")

def get_all_author_links():
    """Collect all unique author profile links from the main listing."""
    author_links = set()
    url = BASE_URL

    while url:
        soup = get_page(url)
        for quote in soup.find_all("div", class_="quote"):
            link = quote.find("a")["href"]
            if "/author/" in link:
                author_links.add(BASE_URL + link)

        next_btn = soup.find("li", class_="next")
        url = BASE_URL + next_btn.a["href"] if next_btn else None

    print(f"Found {len(author_links)} unique profiles")
    return list(author_links)

def scrape_contact(url):
    """
    Scrape a single author/business profile page.
    Returns name, born date, location, description (bio).
    In real use: name, email, phone, address, website, etc.
    """
    soup = get_page(url)

    name = soup.find("h3", class_="author-title")
    born_date = soup.find("span", class_="author-born-date")
    born_location = soup.find("span", class_="author-born-location")
    description = soup.find("div", class_="author-description")

    return {
        "name": name.text.strip() if name else "N/A",
        "born_date": born_date.text.strip() if born_date else "N/A",
        "location": born_location.text.strip() if born_location else "N/A",
        "bio": description.text.strip()[:200] if description else "N/A",
        "profile_url": url,
        "date_scraped": date.today()
    }

def scrape_all_contacts():
    """Scrape all contact profiles."""
    links = get_all_author_links()
    contacts = []

    for i, link in enumerate(links):
        print(f"Scraping profile {i+1}/{len(links)}: {link}")
        contact = scrape_contact(link)
        contacts.append(contact)
        time.sleep(0.5)  # Be polite — don't hammer the server

    return contacts

def save_to_csv(contacts, filename="contacts.csv"):
    """Save contacts to CSV."""
    if not contacts:
        print("No data to save.")
        return

    keys = contacts[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(contacts)

    print(f"\n✅ Done! Saved {len(contacts)} contacts to {filename}")

def search_contacts(contacts, keyword):
    """Search contacts by name or location keyword."""
    return [c for c in contacts if keyword.lower() in c["name"].lower()
            or keyword.lower() in c["location"].lower()]

if __name__ == "__main__":
    print("=== Business Contact Finder by Hussain Farhan ===\n")
    contacts = scrape_all_contacts()
    save_to_csv(contacts)

    # Preview
    print("\nSample contacts:")
    for c in contacts[:3]:
        print(f"  👤 {c['name']} | {c['location']}")
        print(f"     {c['bio'][:80]}...\n")
