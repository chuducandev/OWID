import requests
from bs4 import BeautifulSoup


def crawl_chart_pages(url: str) -> list:
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    target_div = soup.find("div", class_="content")

    links = []
    if target_div:
        for li in target_div.find_all("li"):
            anchor_tags = li.find_all("a")
            for anchor in anchor_tags:
                href = anchor.get("href")
                if href:
                    if href.startswith("https://ourworldindata.org"):
                        links.append(href)
                    else:
                        links.append("https://ourworldindata.org" + href)

    return links
