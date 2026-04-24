import ast
import os
import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    tree = ast.parse(source_code)
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node)
            functions.append({'name': node.name, 'docstring': doc})

    # Find business rule comments
    business_rules = re.findall(r"#\s*(Business Logic Rule[^\n]*)", source_code, flags=re.IGNORECASE)

    document = {
        'document_id': os.path.basename(file_path),
        'content': str({'functions': functions, 'business_rules': business_rules}),
        'source_type': 'Code',
        'author': 'Unknown',
        'timestamp': None,
        'source_metadata': {'functions': functions, 'business_rules': business_rules}
    }

    return document

