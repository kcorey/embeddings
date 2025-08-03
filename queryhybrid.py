
import argparse
import torch
from sentence_transformers import SentenceTransformer, util
import json

def clean_json(data):
    if isinstance(data, dict):
        return {k: clean_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_json(i) for i in data]
    elif isinstance(data, float) and (data != data):  # NaN check
        return ""
    return data

# Command-line arguments
parser = argparse.ArgumentParser(description="Query hybrid embeddings.")
parser.add_argument("query", type=str, help="Query string")
parser.add_argument("-n", type=int, default=5, help="Number of results to return")
parser.add_argument("--score", type=float, default=0.3, help="Minimum score threshold")
parser.add_argument("--type", choices=["idea", "article", "both"], default="both", help="Type filter")
parser.add_argument("--device", choices=["cpu", "cuda", "mps"], default=None, help="Force device")
args = parser.parse_args()

# Determine device
if args.device:
    device = torch.device(args.device)
else:
    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2", device=device)

# Load data
data = []
with open("hybrid_embeddings.jsonl", "r") as f:
    for line in f:
        entry = json.loads(line)
        emb_tensor = torch.tensor(entry["embedding"], dtype=torch.float32)
        data.append((entry, emb_tensor))

# Encode the query
query_emb = model.encode(args.query, convert_to_tensor=True)

# Score and filter
results = []
for meta, emb in data:
    if args.type != "both" and meta.get("type") != args.type:
        continue
    score = float(util.dot_score(query_emb, emb)[0][0])
    if score >= args.score:
        meta["score"] = round(score, 4)
        if "embedding" in meta:
            del meta["embedding"]
        results.append(meta)

# Sort and print
results.sort(key=lambda x: x["score"], reverse=True)
for item in results[:args.n]:
   print(json.dumps(clean_json(item), indent=2, ensure_ascii=False))
