import pandas as pd
import re
from datetime import datetime
import os

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------
    
    # Remove duplicates based on 'id' if present
    if 'id' in df.columns:
        df = df.drop_duplicates(subset=['id'])

    # Clean price column
    def parse_price(x):
        if pd.isna(x):
            return None
        s = str(x).strip()
        # dollar sign
        s = s.replace(',', '')
        m = re.search(r"\$?\s*([0-9]+(?:\.[0-9]+)?)", s)
        if m:
            return float(m.group(1))
        # simple english words (very small set)
        words_to_num = {'five': 5.0, 'ten': 10.0}
        for w, v in words_to_num.items():
            if w in s.lower():
                return v
        # fallback: try cast
        try:
            return float(s)
        except Exception:
            return None

    if 'price' in df.columns:
        df['price_clean'] = df['price'].apply(parse_price)

    # Normalize date_of_sale
    def normalize_date(s):
        if pd.isna(s):
            return None
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
            try:
                return datetime.strptime(str(s), fmt).date().isoformat()
            except Exception:
                continue
        # fallback: return original
        return str(s)

    if 'date_of_sale' in df.columns:
        df['date_norm'] = df['date_of_sale'].apply(normalize_date)

    # Convert to list of unified dicts
    records = []
    for _, row in df.iterrows():
        doc = {
            'document_id': str(row.get('id', 'csv-' + str(_))),
            'content': str(row.to_dict()),
            'source_type': 'CSV',
            'author': 'Unknown',
            'timestamp': None,
            'source_metadata': {
                'price': row.get('price_clean'),
                'date_of_sale': row.get('date_norm')
            }
        }
        records.append(doc)

    return records

