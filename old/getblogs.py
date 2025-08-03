#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://stepituphr.com'
blog_urls = [f"{BASE_URL}/blog/page-{i}" for i in range(1, 140)]  # Adjust for how many blog pages you have

for url in blog_urls:
    print("Processing "+url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    for article in soup.select('article'):  # Adjust selector
        title = article.select_one('h1, h2').get_text(strip=True)
        link = BASE_URL + article.find('a')['href']
        print(title, link)
