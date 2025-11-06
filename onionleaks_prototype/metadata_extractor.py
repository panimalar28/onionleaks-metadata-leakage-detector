
import re, os, json
DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "sample_onion_sites")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "metadata_output.json")

patterns = {
    "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}"),
    "btc_wallet": re.compile(r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b"),
    "pgp_key": re.compile(r"0x[a-fA-F0-9]{8,16}"),
    "timestamp": re.compile(r"\b\d{4}[-T\s]\d{2}:\d{2}:\d{2}\b")
}

def extract_metadata(text):
    results = {}
    for key, pat in patterns.items():
        matches = pat.findall(text)
        results[key] = list(set(matches))
    return results

def main():
    all_data = []
    for file in sorted(os.listdir(DATA_DIR)):
        if not file.lower().endswith(".txt"):
            continue
        path = os.path.join(DATA_DIR, file)
        with open(path, "r") as f:
            text = f.read()
        md = extract_metadata(text)
        all_data.append({"site": file, "content_snippet": text[:240], "metadata": md})
    with open(OUTPUT_FILE, "w") as out:
        json.dump(all_data, out, indent=2)
    print(f"Metadata extracted to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
