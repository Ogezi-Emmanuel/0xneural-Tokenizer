from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

# 1. Initialize the API
app = FastAPI(title="0xNeural BPE Tokenizer Engine")

# 2. Configure CORS (Crucial for Streamlit to talk to this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows any frontend to ping this API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Define the payload structure strictly
class ContractPayload(BaseModel):
    source_code: str

# 4. Rebuild the core mathematical logic
def get_stats(ids):
    counts = {}
    for pair in zip(ids, ids[1:]):
        counts[pair] = counts.get(pair, 0) + 1
    return counts

def merge(ids, pair, idx):
    newids = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
            newids.append(idx)
            i += 2
        else:
            newids.append(ids[i])
            i += 1
    return newids

# 5. Global Memory State
class API_Tokenizer:
    def __init__(self):
        self.merges = {}
        self.vocab = {idx: bytes([idx]) for idx in range(256)}
        # Load the weights relative to the script location
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "web3_tokenizer_2000_merges.json")
        self.load_weights(file_path)

    def load_weights(self, path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
            
            for pair_str, idx in data["merges"].items():
                p0, p1 = map(int, pair_str.split("|"))
                self.merges[(p0, p1)] = idx
        except Exception as e:
            print(f"FATAL ERROR loading weights: {e}")

    def encode(self, text):
        ids = list(text.encode("utf-8"))
        while len(ids) >= 2:
            stats = get_stats(ids)
            pair = min(stats, key=lambda p: self.merges.get(p, float("inf")), default=None)
            if pair not in self.merges:
                break
            idx = self.merges[pair]
            ids = merge(ids, pair, idx)
        return ids

# Instantiate the engine in global memory instantly on boot
tokenizer_engine = API_Tokenizer()

# 6. Expose the Ingestion Funnel
@app.post("/api/v1/encode")
async def encode_contract(payload: ContractPayload):
    if not payload.source_code:
        raise HTTPException(status_code=400, detail="Empty source code payload")
    
    compressed_ids = tokenizer_engine.encode(payload.source_code)
    
    return {
        "status": "success",
        "original_bytes": len(payload.source_code),
        "token_count": len(compressed_ids),
        "tokens": compressed_ids
    }

@app.get("/")
async def health_check():
    return {"status": "Tokenizer API is live and listening."}