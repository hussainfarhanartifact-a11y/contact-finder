# Business Contact Finder
**By Hussain Farhan**

Automatically discovers and scrapes all business profile pages from a directory site. Extracts name, location, bio and contact details and exports everything to CSV.

## What it does
- Auto-discovers all profile links from listing pages
- Visits each profile and extracts full details
- Search and filter contacts by name or location
- Polite rate limiting so it doesn't get blocked
- Saves to contacts.csv

## How to run

Install dependencies:
pip install requests beautifulsoup4

Run it:
python contact_finder.py

Filter by location:
results = search_contacts(contacts, "Karachi")

## Output
| name | location | bio | profile_url | date_scraped |
|------|----------|-----|-------------|--------------|
| Ahmed Khan | Karachi | Experienced... | https://... | 2024-01-01 |

## Tech used
Python · Requests · BeautifulSoup4

## Hire me
📧 hussainfarhanartifact@gmail.com
🌐 Fiverr: fiverr.com/hussainfarhan_d
