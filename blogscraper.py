import os
import requests
import time
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pathlib import Path

SITEMAP_URL = "https://www.stepituphr.com/blog-posts-sitemap.xml"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Mac OS X) Python bot"}
IMAGES_DIR = "images"
OUTPUT_JSON = "articles.json"

os.makedirs(IMAGES_DIR, exist_ok=True)

def sanitize_filename(url):
    return os.path.basename(urlparse(url).path).split("?")[0]

def download_image(img_url):
    filename = sanitize_filename(img_url)
    path = os.path.join(IMAGES_DIR, filename)
    if not os.path.exists(path):
        try:
            res = requests.get(img_url, headers=HEADERS, timeout=10)
            with open(path, "wb") as f:
                f.write(res.content)
        except Exception as e:
            print(f"⚠️ Error downloading {img_url}: {e}")
            return None
    return path

def scrape_article(url, fallback_date, image_url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.find("h1").get_text(strip=True)

        meta_author = soup.find("meta", {"name": "author"})
        author = meta_author["content"].strip() if meta_author else "Unknown"

        meta_date = soup.find("meta", {"property": "article:published_time"})
        published = meta_date["content"] if meta_date else fallback_date

        article = soup.find("article") or soup.find("div", class_="blog-post-body")
        content = article.get_text(separator="\n", strip=True) if article else "[No content found]"

        print(f"📄 {title}")

        return {
            "url": url,
            "title": title,
            "author": author,
            "published_date": published,
            "content": content,
            "image_url": image_url
        }

    except Exception as e:
        print(f"❌ Failed to scrape {url}: {e}")
        return None

def parse_sitemap():
    res = requests.get(SITEMAP_URL)
    tree = ET.fromstring(res.content)
    ns = {
        "ns": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "image": "http://www.google.com/schemas/sitemap-image/1.1"
    }

    articles = []
    for url in tree.findall("ns:url", ns):
        loc = url.find("ns:loc", ns).text
        lastmod_elem = url.find("ns:lastmod", ns)
        lastmod = lastmod_elem.text if lastmod_elem is not None else None

        img_elem = url.find("image:image/image:loc", ns)
        img_url = img_elem.text if img_elem is not None else None

        if img_url:
            download_image(img_url)

        article_data = scrape_article(loc, lastmod, img_url)
        if article_data:
            articles.append(article_data)

        time.sleep(1)  # Be polite

    return articles

if __name__ == "__main__":
    all_articles = parse_sitemap()

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, indent=2, ensure_ascii=False)

    print(f"✅ Scraped {len(all_articles)} articles. Data saved to {OUTPUT_JSON}")
