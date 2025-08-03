#!/usr/bin/env python3
# query_ideas.py

import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sys

# Load saved ideas and embeddings
with open("idea_embeddings.json", "r") as f:
    data = json.load(f)

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Accept query from command-line
if len(sys.argv) < 2:
    print("Usage: python query_ideas.py \"your search phrase here\"")
    exit()

query_text = " ".join(sys.argv[1:])
query_embedding = model.encode([query_text])[0]

# Compute cosine similarity
def get_similarity(a, b):
    return cosine_similarity([a], [b])[0][0]

# Rank ideas
results = [
    {"idea": item["idea"], "score": get_similarity(query_embedding, np.array(item["embedding"]))}
    for item in data
]
results.sort(key=lambda x: x["score"], reverse=True)

# Show top matches
print(f"\nTop matches for: '{query_text}'\n")
for r in results[:5]:
    print(f"({r['score']:.3f}) {r['idea']}")
