
import argparse
import json
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--blog_json', type=str, default='stepituphr_blog_posts.json')
parser.add_argument('--ideas_csv', type=str, default='Endless Post Ideas.csv')
parser.add_argument('--out', type=str, default='hybrid_embeddings.jsonl')
args = parser.parse_args()

import pandas as pd

model = SentenceTransformer('all-MiniLM-L6-v2')

out_f = open(args.out, 'w')

# Process blog posts
with open(args.blog_json) as f:
    blog_posts = json.load(f)

for post in tqdm(blog_posts, desc="Embedding articles"):
    content = post.get("full_content", "")
    if not content.strip():
        continue
    emb = model.encode(content).tolist()
    enriched = {
        "type": "article",
        "date Pub": post.get("published", ""),
        "status": "Open",
        "pubauthor": "",
        "origauthor": "Debra Corey",
        "theme": "Recognition",
        "idea": post.get("title", ""),
        "details": post.get("summary", ""),
        "news1": "",
        "news2": "",
        "news3": "",
        "article": content,
        "image": "",
        "title": post.get("title", ""),
        "url": post.get("url", ""),
        "published": post.get("published", ""),
        "summary": post.get("summary", ""),
        "embedding": emb
    }
    out_f.write(json.dumps(enriched) + '\n')

# Process idea CSV
df = pd.read_csv(args.ideas_csv)
for _, row in tqdm(df.iterrows(), total=len(df), desc="Embedding ideas"):
    text = str(row.get("Idea", ""))
    if not text.strip():
        continue
    emb = model.encode(text).tolist()
    enriched = row.to_dict()
    enriched.update({
        "Type": "idea",
        "embedding": emb
    })
    out_f.write(json.dumps(enriched) + '\n')

out_f.close()
