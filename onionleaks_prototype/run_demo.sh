
#!/bin/bash
python metadata_extractor.py
python osint_matcher.py
streamlit run app.py
