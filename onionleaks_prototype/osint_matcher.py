
import os, json
BASE = os.path.dirname(__file__)
INPUT_FILE = os.path.join(BASE, "metadata_output.json")
OUTPUT_FILE = os.path.join(BASE, "correlations.json")

# Fake OSINT DB (for demo). In real usage, replace with actual OSINT sources/APIs.
OSINT_DB = {
    "emails": ["darkking@protonmail.com", "cyberhunter@mail.com", "shadow.seller@mail.com"],
    "wallets": ["1BoatSLRHtKNngkdXEeobR76b53LETtpyT", "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy"],
    "pgp_keys": ["0x9C123456", "0xDEADBEEF"]
}

def load_data():
    with open(INPUT_FILE) as f:
        return json.load(f)

def correlate(data):
    results = []
    for entry in data:
        matched = {"site": entry["site"], "matches": [], "score": 0}
        for e in entry["metadata"].get("email", []):
            if e in OSINT_DB["emails"]:
                matched["matches"].append({"type": "email", "value": e})
        for w in entry["metadata"].get("btc_wallet", []):
            if w in OSINT_DB["wallets"]:
                matched["matches"].append({"type": "wallet", "value": w})
        for p in entry["metadata"].get("pgp_key", []):
            if p in OSINT_DB["pgp_keys"]:
                matched["matches"].append({"type": "pgp_key", "value": p})
        # simple scoring: 10 points per match
        matched["score"] = len(matched["matches"]) * 10
        if matched["matches"]:
            results.append(matched)
    return results

def main():
    data = load_data()
    correlated = correlate(data)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(correlated, f, indent=2)
    print(f"Correlations saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
