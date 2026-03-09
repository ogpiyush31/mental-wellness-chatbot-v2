import json
import faiss
import numpy as np
import pickle


with open("mental_awareness_60_trees_kb.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Total nodes loaded:", len(data))

vectors = []
metadata = []



for item in data:

    
    if "vector" not in item:
        continue

    vectors.append(item["vector"])

    metadata.append({
        "node_id": item.get("node_id"),
        "type": item.get("type"),
        "question": item.get("question", ""),
        "response": item.get("response", ""),
        "followups": item.get("followups", []),
        "search_text": item.get("search_text", "")
    })


vectors = np.array(vectors).astype("float32")

print("Vector shape:", vectors.shape)


dimension = vectors.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(vectors)

print("Total vectors in index:", index.ntotal)


faiss.write_index(index, "mental_index.faiss")


with open("metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print("✅ FAISS index and metadata saved successfully!")