OnionLeaks Prototype (Simulation) - Professional Demo
====================================================

Files included:
- metadata_extractor.py     : Extracts emails, BTC wallets, PGP keys, timestamps from sample onion site text files.
- osint_matcher.py         : Simulated OSINT correlation against a fake OSINT DB.
- app.py                   : Streamlit dashboard to view extracted metadata and correlation results (professional style).
- data/sample_onion_sites/ : 10 sample .txt files (simulated onion site content).
- metadata_output.json     : Produced by running metadata_extractor.py
- correlations.json        : Produced by running osint_matcher.py
- run_demo.sh              : Simple bash script to run everything in sequence (optional).

Prerequisites:
- Python 3.8+
- Recommended packages:
    pip install streamlit pandas networkx matplotlib

Quick run steps (recommended for demo laptop):
1. Open a terminal and navigate to this folder.
2. Run: python metadata_extractor.py
3. Run: python osint_matcher.py
4. Run: streamlit run app.py
5. The Streamlit app will open in your browser (http://localhost:8501 by default).

Notes:
- This is a simulation using safe sample data; do NOT use it to crawl the live Tor network without appropriate legal approvals.
- To adapt to real data, replace OSINT_DB in osint_matcher.py with actual OSINT data sources/APIs and ensure legal compliance.

Good luck at TN Police Hackathon 2025!
