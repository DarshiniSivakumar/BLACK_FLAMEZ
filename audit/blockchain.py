import json
import hashlib
import time
import os

LOG_FILE = "audit/audit_log.json"

def load_chain():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        return json.load(f)

def save_chain(chain):
    with open(LOG_FILE, "w") as f:
        json.dump(chain, f, indent=2)

def create_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

def add_audit_entry(decision):
    chain = load_chain()
    previous_hash = chain[-1]["current_hash"] if chain else "0"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    decision_hash = create_hash(json.dumps(decision, sort_keys=True))
    block_string = previous_hash + decision_hash + timestamp
    current_hash = create_hash(block_string)

    block = {
        "index": len(chain) + 1,
        "timestamp": timestamp,
        "decision_summary": decision,
        "previous_hash": previous_hash,
        "current_hash": current_hash
    }

    chain.append(block)
    save_chain(chain)
    return block

def verify_chain():
    chain = load_chain()
    for i in range(1, len(chain)):
        prev = chain[i - 1]
        curr = chain[i]

        recalculated_hash = create_hash(
            curr["previous_hash"]
            + create_hash(json.dumps(curr["decision_summary"], sort_keys=True))
            + curr["timestamp"]
        )

        if curr["current_hash"] != recalculated_hash:
            return False
    return True
