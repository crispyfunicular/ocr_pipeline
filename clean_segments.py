#!/usr/bin/env python3
import sys
import json
import re
from pathlib import Path

def clean_text(text):
    if not isinstance(text, str):
        return text
        
    # 0. Remplace les retours à la ligne par des espaces
    text = text.replace('\n', ' ')
    
    # 1. Supprime la numérotation initiale (chiffres suivis optionnellement de points, tirets, parenthèses ou espaces)
    text = re.sub(r'^\s*\d+[\s.\-)]*', '', text)
    
    # 2. Supprime la ponctuation finale si la longueur du segment (avant nettoyage de la fin) est < 20 caractères
    if len(text) < 20:
        # On enlève la ponctuation finale courante (. , ; : ! ?) et les espaces éventuels
        text = text.rstrip('.,;:!? ')
        
    text = text.strip()
    
    # 3. Supprime les guillemets orphelins (« ou »)
    # On regarde si on a une ouverture sans fermeture, ou une fermeture sans ouverture
    has_open = text.startswith('«')
    has_close = text.endswith('»')
    
    if has_open and not has_close:
        text = text[1:].lstrip()
    elif has_close and not has_open:
        text = text[:-1].rstrip()
        
    return text

def process_file(filepath):
    cleaned_lines = []
    modified_count = 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                cleaned_lines.append(line)
                continue
                
            try:
                data = json.loads(line)
                new_data = {}
                row_modified = False
                
                for key, value in data.items():
                    if isinstance(value, str):
                        cleaned_val = clean_text(value)
                        new_data[key] = cleaned_val
                        if cleaned_val != value.strip():
                            row_modified = True
                    else:
                        new_data[key] = value
                        
                cleaned_lines.append(json.dumps(new_data, ensure_ascii=False) + '\n')
                if row_modified:
                    modified_count += 1
            except json.JSONDecodeError:
                print(f"Erreur de lecture JSON à la ligne {line_num} dans {filepath}")
                cleaned_lines.append(line)
                
    if modified_count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)
        print(f"[{filepath.name}] Mis à jour : {modified_count} segment(s) modifié(s).")
    else:
        print(f"[{filepath.name}] Aucune modification nécessaire.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python clean_segments.py <dossier_ou_fichier>")
        sys.exit(1)
        
    target = Path(sys.argv[1])
    
    if target.is_file():
        if target.suffix == '.jsonl':
            process_file(target)
        else:
            print(f"Le fichier {target} n'est pas un fichier .jsonl")
    elif target.is_dir():
        jsonl_files = list(target.rglob('*.jsonl'))
        if not jsonl_files:
            print(f"Aucun fichier .jsonl trouvé dans le dossier {target}")
            
        for filepath in jsonl_files:
            process_file(filepath)
    else:
        print(f"Erreur : {target} introuvable.")
        sys.exit(1)

if __name__ == "__main__":
    main()
