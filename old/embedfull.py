#!/usr/bin/env python3

import csv, json, hashlib
from pathlib import Path
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# === CONFIGURATION ===
IDEAS_CSV = "Endless Post Ideas.csv"
ARTICLES_JSON = "stepituphr_blog_posts.json"
EMBEDDING_OUTPUT = "hybrid_embeddings.jsonl"
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

def get_embedding(text):
    return model.encode(text).tolist()

def hash_input(text):
    return hashlib.md5(text.encode()).hexdigest()

def load_existing_inputs(path):
    seen = set()
    if Path(path).exists():
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    seen.add(hash_input(obj["embedding_input"]))
                except Exception:
                    continue
    return seen

def load_ideas(csv_path):
    ideas = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            idea = row.get("Idea", "").strip()
            if idea:
                ideas.append({
                    "type": "idea",
                    "embedding_input": idea,
                    "source": {k: v for k, v in row.items()}
                })
    return ideas

def load_articles(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [
        {
            "type": "article",
            "embedding_input": item["full_content"].strip(),
            "source": item
        }
        for item in data if item.get("full_content")
    ]

def main():
    print("🔍 Loading inputs...")
    all_items = load_ideas(IDEAS_CSV) + load_articles(ARTICLES_JSON)
    seen_hashes = load_existing_inputs(EMBEDDING_OUTPUT)

    new_items = [item for item in all_items if hash_input(item["embedding_input"]) not in seen_hashes]
    print(f"✨ {len(new_items)} new items to embed")

    with open(EMBEDDING_OUTPUT, "a", encoding="utf-8") as out_file:
        for item in tqdm(new_items):
            try:
                embedding = get_embedding(item["embedding_input"])
                out_record = {
                    "type": item["type"],
                    "embedding_input": item["embedding_input"],
                    "embedding": embedding,
                    "source": item["source"]
                }
                out_file.write(json.dumps(out_record) + "\n")
            except Exception as e:
                print(f"❌ Failed to embed: {e}")

    print(f"✅ Local embedding complete. Saved to: {EMBEDDING_OUTPUT}")

if __name__ == "__main__":
    main()
