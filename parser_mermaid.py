import re
import os
import csv

def mermaid_parser(code_text):
 
    verifyClassDiagram = bool(re.search(r'classDiagram', code_text))
    
    # nr de clase
    classes = re.findall(r'class\s+(\w+)\s*\{', code_text)
    nr_classes = len(classes)
    
    # nr de variabile
    attributes = re.findall(r'^[ \t]*[+\-#~]\s*[^()\n]+$', code_text, re.MULTILINE)
    nr_attributes = len(attributes)
    
    # nr de metode
    methods = re.findall(r'^[ \t]*[+\-#~]?\s*[a-zA-Z0-9_]+\s*[a-zA-Z0-9_]+\s*\([^)]*\)', code_text, re.MULTILINE)
    nr_methods = len(methods)
    
    # nr, tipuri de relații
    rel = re.findall(r'(\w+)\s*(?:"[^"]*")?\s*(<\|--|--\|>|\*--|--\*|o--|--o|-->|<--|--)\s*(?:"[^"]*")?\s*(\w+)', code_text)
    nr_rel = len(rel)
    
    nr_asocieri = 0
    nr_compozitii = 0
    nr_mosteniri = 0
    
    for r in rel:
        sageata = r[1] # r[1] este tipul săgeții extrase (ex: --> sau *--)
        if sageata in ['<|--', '--|>']:
            nr_mosteniri += 1
        elif sageata in ['*--', '--*']:
            nr_compozitii += 1
        elif sageata in ['-->', '<--', '--']:
            nr_asocieri += 1
    
    return {
        "Format Mermaid valid": verifyClassDiagram,
        "Numarul total de clase gasite": nr_classes,
        "Numele claselor": classes,
        "Numarul total de atribute": nr_attributes,
        "Numarul total de metode": nr_methods,
        "Numarul total de relatii": nr_rel,
        "Asocieri simple (-->)": nr_asocieri,
        "Compozitii (*--)": nr_compozitii,
        "Mosteniri (<|--)": nr_mosteniri,
        "Lista relatii": [(r[0], r[1], r[2]) for r in rel] 
    }

# TESTARE

def main():
    nume_fisier = "cod_mermaid.txt"
    fisier_export = "rezultate.csv"
    
    if not os.path.exists(nume_fisier):
        print(f"Eroare: Fisierul '{nume_fisier}' nu a fost gasit!")
        return

    with open(nume_fisier, 'r', encoding='utf-8') as fisier:
        cod_diag = fisier.read()
        
    print(f"Rezultate analiza pentru fisierul: '{nume_fisier}' ---\n")
    rez = mermaid_parser(cod_diag)
    
    for metrica, val in rez.items():
        if isinstance(val, list):
            print(f"{metrica}:")
            for item in val:
                print(f"  - {item}")
        else:
            print(f"{metrica}: {val}")

    # pregatire date pt excel (err tupluri)
    for key, valoare in rez.items():
        if isinstance(valoare, list):
            if len(valoare) > 0 and isinstance(valoare[0], tuple):
                rez[key] = ", ".join([f"{r[0]} {r[1]} {r[2]}" for r in valoare])
            else:
                rez[key] = ", ".join(str(v) for v in valoare)
                
    write_header = not os.path.exists(fisier_export) or os.path.getsize(fisier_export) == 0
                
    # scriere cu append 
    with open(fisier_export, mode='a', newline='', encoding='utf-8') as f_csv:
        writer = csv.writer(f_csv)
        
        if write_header:
            writer.writerow(rez.keys())   # cap tabel 
            
        writer.writerow(rez.values())     # rezultate
        
    print(f"\nFisierul cu rezultate a fost actualizat cu succes: '{fisier_export}'")

if __name__ == "__main__":
    main()