import re
import os

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
        # Remove common noise tokens like [Music], [inaudible], [Laughter], case insensitive
        text = re.sub(r"\[(?:music|inaudible|laughter|applause|laughs)\]", "", text, flags=re.IGNORECASE)

        # Remove timestamps like [00:00:00] or (00:00)
        text = re.sub(r"\[?\(?\d{1,2}:\d{2}(?::\d{2})?\)?\]?", "", text)

        # Collapse multiple whitespace
        text = re.sub(r"\s+", " ", text).strip()

        # Try to find a Vietnamese-written price, e.g., "năm trăm nghìn" or numeric like 500000
        # A simple approach: look for sequences of Vietnamese number words (một|hai|...|nghìn|triệu|tỷ)
        vn_number_words = r"(?:một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mươi|trăm|nghìn|triệu|tỷ)"
        match = re.search(rf"((?:{vn_number_words}|\s)+nghìn|(?:{vn_number_words}|\s)+triệu|\d[\d,\.]+)", text, flags=re.IGNORECASE)
        price_found = None
        if match:
            price_found = match.group(0).strip()

        # Try to convert Vietnamese number words to integer VND
        def vn_words_to_int(s: str):
            if not s:
                return None
            s = s.lower().replace('-', ' ')
            token_map = {
                'một': 1, 'mot': 1, 'hai': 2, 'ba': 3, 'bốn': 4, 'bon': 4, 'năm': 5, 'nam': 5,
                'sáu': 6, 'sau': 6, 'bảy': 7, 'bay': 7, 'tám': 8, 'tam': 8, 'chín': 9, 'chin': 9,
                'mười': 10, 'muoi': 10
            }
            multipliers = {
                'mươi': 10, 'mươi': 10, 'mươi': 10, 'mười': 10, 'trăm': 100, 'nghìn': 1000, 'nghin': 1000,
                'triệu': 1000000, 'trieu': 1000000, 'tỷ': 1000000000, 'ty': 1000000000
            }

            parts = s.split()
            total = 0
            partial = 0
            for p in parts:
                p = p.strip()
                if not p:
                    continue
                if p in token_map:
                    partial += token_map[p]
                else:
                    # try numeric token
                    try:
                        val = int(p.replace(',', '').replace('.', ''))
                        partial += val
                        continue
                    except Exception:
                        pass

                    if p in multipliers:
                        mult = multipliers[p]
                        if mult >= 1000:
                            # scale the current partial by multiplier
                            if partial == 0:
                                partial = 1
                            total += partial * mult
                            partial = 0
                        else:
                            if partial == 0:
                                partial = 1
                            partial = partial * mult
                    else:
                        # unknown token: skip
                        continue

            total += partial
            if total == 0:
                return None
            return total

        detected_price = None
        if price_found:
            # price_found may be numeric like '500,000' or words like 'năm trăm nghìn'
            # try to parse numeric first
            num = None
            try:
                num = int(re.sub(r"[^0-9]", "", price_found))
            except Exception:
                num = None

            if num and num > 0:
                detected_price = num
            else:
                detected_price = vn_words_to_int(price_found)

        document = {
            "document_id": os.path.basename(file_path),
            # mark as Video so forensic agent picks it up (transcript of video)
            "content": text,
            "source_type": "Video",
            "author": "Unknown",
            "timestamp": None,
            "source_metadata": {"price_mention": price_found, "detected_price_vnd": detected_price}
        }

        return document
    
    return {}

