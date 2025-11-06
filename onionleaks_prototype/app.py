
import streamlit as st
import os, json, pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="OnionLeaks - Prototype", layout="wide")

BASE = os.path.dirname(__file__)
META_FILE = os.path.join(BASE, "metadata_output.json")
CORR_FILE = os.path.join(BASE, "correlations.json")

st.title("🧅 OnionLeaks — Metadata Leakage Detector (Prototype)")
st.markdown("**Professional demo / simulation for TN Police Hackathon 2025**")
st.markdown("---")

if not os.path.exists(META_FILE):
    st.warning("metadata_output.json not found. Run `python metadata_extractor.py` first.")
else:
    with open(META_FILE) as f:
        data = json.load(f)
    # Show extracted metadata summary table
    rows = []
    for d in data:
        site = d["site"]
        emails = ", ".join(d["metadata"].get("email", [])) or "-"
        wallets = ", ".join(d["metadata"].get("btc_wallet", [])) or "-"
        pgp = ", ".join(d["metadata"].get("pgp_key", [])) or "-"
        rows.append({"site": site, "emails": emails, "wallets": wallets, "pgp_keys": pgp})
    df = pd.DataFrame(rows)
    st.subheader("Extracted Metadata")
    st.dataframe(df, use_container_width=True)

st.markdown("---")
st.subheader("OSINT Correlation Results")
if not os.path.exists(CORR_FILE):
    st.info("No correlations found yet. Run `python osint_matcher.py` to generate correlations.")
else:
    with open(CORR_FILE) as f:
        corr = json.load(f)
    if not corr:
        st.write("No matches found in the OSINT database.")
    else:
        # Flatten results for display
        flat = []
        for c in corr:
            for m in c["matches"]:
                flat.append({"site": c["site"], "type": m["type"], "value": m["value"], "score": c["score"]})
        cdf = pd.DataFrame(flat)
        st.dataframe(cdf, use_container_width=True)

        # Simple bar chart: scores per site
        score_df = pd.DataFrame([{"site": c["site"], "score": c["score"]} for c in corr])
        st.markdown("**Match Confidence Scores**")
        fig, ax = plt.subplots()
        ax.bar(score_df["site"], score_df["score"])
        ax.set_xlabel("Site")
        ax.set_ylabel("Score")
        ax.set_title("OSINT Match Confidence per Site")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

        # Network graph: sites <-> matched entities
        G = nx.Graph()
        for c in corr:
            G.add_node(c["site"], type="site")
            for m in c["matches"]:
                node_label = f"{m['type']}:{m['value']}"
                G.add_node(node_label, type=m['type'])
                G.add_edge(c["site"], node_label)
        st.markdown("**Linkage Graph**")
        fig2, ax2 = plt.subplots(figsize=(8,6))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, ax=ax2)
        st.pyplot(fig2)

st.markdown("---")
st.caption("Demo notes: This is a simulation using sample data and a fake OSINT DB. Replace OSINT_DB in osint_matcher.py with real sources for production.")
