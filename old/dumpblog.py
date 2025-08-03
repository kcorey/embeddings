import feedparser
import requests
from bs4 import BeautifulSoup
import json
import time

FEED_URL = "https://www.stepituphr.com/blog-feed.xml"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Mac OS X) Python bot"}

def extract_full_content(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # Adjust selectors to match your blog's HTML structure
        title = soup.find("h1").get_text(strip=True)
        article = soup.find("article")
        if not article:
            article = soup.find("div", class_="blog-post-body")  # Fallback selector
        content = article.get_text(separator="\n", strip=True) if article else "[No content found]"

        return {
            "title": title,
            "url": url,
            "content": content
        }
    except Exception as e:
        print(f"⚠️ Error scraping {url}: {e}")
        return {
            "title": "[Error]",
            "url": url,
            "content": "[Failed to fetch content]"
        }

def parse_feed():
    print(f"📥 Fetching RSS feed: {FEED_URL}")
    feed = feedparser.parse(FEED_URL)
    print(f"✅ Found {len(feed.entries)} entries")
    
    posts = []
    for entry in feed.entries:
        print(f"🔗 Processing: {entry.title}")
        post_data = {
            "title": entry.title,
            "url": entry.link,
            "published": entry.published,
            "summary": entry.summary
        }

        # Optional: fetch full content
        full_data = extract_full_content(entry.link)
        post_data["full_content"] = full_data["content"]
        time.sleep(1)  # Polite delay between requests
        posts.append(post_data)
    
    return posts

if __name__ == "__main__":
    all_posts = parse_feed()

    with open("stepituphr_blog_posts.json", "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)

    print(f"📦 Saved {len(all_posts)} posts to stepituphr_blog_posts.json")
