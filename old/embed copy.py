#!/usr/bin/env python3
# save_embeddings.py

from sentence_transformers import SentenceTransformer
import json

# List of ideas
ideas = [
    "It's a lot like riding a horse, if it's comfortable, you're doing it wrong.",
    "That's the thing about coincidences: sometimes they just happen.",
    "Coaching is about helping someone be the absolute best version of themselves",
    "Be curious, not judgemental",
    ...
]

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
embeddings = model.encode(ideas)

# Save to JSON
data = [{"idea": idea, "embedding": emb.tolist()} for idea, emb in zip(ideas, embeddings)]
with open("idea_embeddings.json", "w") as f:
    json.dump(data, f, indent=2)

print("Saved embeddings to idea_embeddings.json")
