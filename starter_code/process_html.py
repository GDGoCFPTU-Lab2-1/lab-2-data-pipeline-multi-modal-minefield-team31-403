from bs4 import BeautifulSoup
import os

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    table = soup.find('table', id='main-catalog')
    if table is None:
        return []

    rows = []
    for tr in table.find_all('tr'):
        cols = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
        if not cols:
            continue
        # Expect columns like [id, name, price, desc]
        row = {'raw_cols': cols}
        # handle price heuristics
        if len(cols) >= 3:
            price = cols[2]
            if price.lower() in ('n/a', 'liên hệ', 'lien he', 'contact'):
                price_val = None
            else:
                # strip currency symbols
                price_val = price.replace(',', '').replace('$', '').strip()
                try:
                    price_val = float(price_val)
                except Exception:
                    price_val = price
            row['price'] = price_val
        rows.append(row)

    docs = []
    for i, r in enumerate(rows):
        docs.append({
            'document_id': f'html-{i}',
            'content': str(r),
            'source_type': 'HTML',
            'author': 'Unknown',
            'timestamp': None,
            'source_metadata': r
        })

    return docs
    # ------------------------------------------
    
    # TODO: Use BeautifulSoup to find the table with id 'main-catalog'
    # TODO: Extract rows, handling 'N/A' or 'Liên hệ' in the price column.
    # TODO: Return a list of dictionaries for the UnifiedDocument schema.
    
    return []

