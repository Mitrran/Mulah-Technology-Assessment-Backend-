import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from urllib.parse import urljoin
import json

url = 'https://www.theverge.com/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
articles = soup.find_all('a', class_='group hover:text-white')

headlines = []

for article in articles:
    aria_label = article.get('aria-label', '')

    # Check if aria-label is present
    if aria_label:
        title = aria_label
        href = article.get('href', '')

        # If href is relative, convert to absolute URL
        link = urljoin(url, href)

        # Find the time tag and extract pub_date_str if it exists
        time_tag = article.find_next('time')
        pub_date_str = time_tag['datetime'] if time_tag else None

        if pub_date_str:
            # Parse the datetime string without the UTC offset
            pub_date = datetime.strptime(pub_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')

            # Add the UTC timezone to the datetime object
            pub_date = pub_date.replace(tzinfo=timezone.utc)

            # Set UTC offset to +8 hours
            pub_date = pub_date + timedelta(hours=8)

            # Manually construct the formatted pub_date string with the GMT+8 offset
            formatted_pub_date = pub_date.strftime('%b %d, %Y at %I:%M %p GMT+8')
        else:
            formatted_pub_date = None

        # Articles details
        headlines.append({
            "title": title,
            "link": link,
            "pub_date": formatted_pub_date,
            "aria_label": aria_label,
            "href": href,
        })

# Sort the headlines based on publication date in descending order
headlines = sorted(headlines, key=lambda x: datetime.strptime(x['pub_date'], '%b %d, %Y at %I:%M %p GMT+8'), reverse=True)

# Save headlines to a JSON file
with open('ArticleHeadlines.json', 'w') as json_file:
    json.dump(headlines, json_file, indent=2)
