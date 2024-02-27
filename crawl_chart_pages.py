import requests
from bs4 import BeautifulSoup

# Define the target URL
url = "https://ourworldindata.org/charts"

# Send a GET request
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the target unordered list
target_section = soup.find("section", id="explorers-section")

# Check if the list is found
if target_section:
    # Extract links from all li tags within the ul
    links = []
    for li in target_section.find_all("li"):
        # Find anchor tags within each li
        anchor_tags = li.find_all("a")
        for anchor in anchor_tags:
            # Extract href attribute if it exists
            href = anchor.get("href")
            if href:
                links.append(href)

    # Print the extracted links
    if links:
        print("Extracted links:")
        for link in links:
            print(link)
    else:
        print("No links found within the target section.")
else:
    print("Target ul element not found.")
