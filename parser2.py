import re
import os
import csv

def mermaid_parser2(code_text):
    verifyClassDiagram = bool(re.search(r'classDiagram', code_text))

    # gasire clase
    class_blocks = re.findall(r'class\s+(\w+)\s*\{([^}]*)\}', code_text)
    
    nume_clase = []
    for nume_clasa, continut in class_blocks:
        # verif clasa abstracta
        if re.search(r'<<abstract>>', continut, re.IGNORECASE):
            nume_clase.append(f"{nume_clasa} (Abstract)")
        else:
            nume_clase.append(nume_clasa)
    
    detalii_atrb = []
    detalii_met = []

    # analiza atribute + metode
    for nume_clasa, continut in class_blocks:
        atrb = re.findall(r'^[ \t\xa0]*([+\-#~])?\s*([a-zA-Z_][^()\n]*)$', continut, re.MULTILINE)
        for viz, denumire in atrb:
            viz = viz if viz else "lipsa"
            detalii_atrb.append(f"{nume_clasa} -> [{viz}] {denumire.strip()}")
            
        met = re.findall(r'^[ \t]*([+\-#~])?\s*(.*?\([^)]*\).*)$', continut, re.MULTILINE)
        for viz, denumire in met:
            viz = viz if viz else "lipsa"
            detalii_met.append(f"{nume_clasa} -> [{viz}] {denumire.strip()}")

    # gasire relatii
    rel_rgx = r'(\w+)\s*(?:"([^"]*)")?\s*(<\|--|--\|>|\*--|--\*|o--|--o|-->|<--|--)\s*(?:"([^"]*)")?\s*(\w+)'
    rel = re.findall(rel_rgx, code_text)
    
    detalii_rel = []
    nr_asocieri = nr_compozitii = nr_mosteniri = 0
    
    for r in rel:
        sursa, mult_sursa, arrow, mult_dest, dest = r
        m1 = mult_sursa if mult_sursa else "-"
        m2 = mult_dest if mult_dest else "-"
        
        detalii_rel.append(f"{sursa}[{m1}] {arrow} {dest}[{m2}]")
        
        if arrow in ['<|--', '--|>']: nr_mosteniri += 1
        elif arrow in ['*--', '--*']: nr_compozitii += 1
        elif arrow in ['-->', '<--', '--']: nr_asocieri += 1
        
    return {
        "Format valid": verifyClassDiagram,
        "Clase gasite": nume_clase,
        "Total Atribute": len(detalii_atrb),
        "Lista Atribute (Viz | Denumire)": detalii_atrb,
        "Total Metode": len(detalii_met),
        "Lista Metode (Viz | Denumire)": detalii_met,
        "Total Relatii": len(rel),
        "Tipuri Relatii (A/C/M)": f"A:{nr_asocieri} | C:{nr_compozitii} | M:{nr_mosteniri}",
        "Detalii Relatii (Multiplicitati)": detalii_rel
    }


def main():
    # gestionare fisiere
    curent_dir = os.path.dirname(os.path.abspath(__file__))
    nume_fisier = os.path.join(curent_dir, "cod_mermaid.txt")
    fisier_exp_csv = os.path.join(curent_dir, "rezultate2.csv")
    fisier_raport_txt = os.path.join(curent_dir, "raport_evaluare.txt") 
    
    if not os.path.exists(nume_fisier):
        print(f"Fisierul '{nume_fisier}' nu a fost gasit")
        return

    # citire fisier
    with open(nume_fisier, 'r', encoding='utf-8') as fisier:
        cod_diag = fisier.read()
        
    rez = mermaid_parser2(cod_diag)

    # afisare + salvare raport fisier text
    print(f"\nREZULTATE ANALIZA PT: '{nume_fisier}'\n")
    for metrica, val in rez.items():
        if isinstance(val, list):
            print(f"{metrica}:")
            for item in val:
                print(f"  - {item}")
        else:
            print(f"{metrica}: {val}")

    with open(fisier_raport_txt, 'w', encoding='utf-8') as f_txt:
        f_txt.write(f"--RAPORT EVALUARE--\n")
        for metrica, val in rez.items():
            if isinstance(val, list):
                f_txt.write(f"{metrica}:\n")
                for item in val:
                    f_txt.write(f"  - {item}\n")
            else:
                f_txt.write(f"{metrica}: {val}\n")
        f_txt.write("\n--------------------\n")

    # salvare in excel (fisier csv)
    for key, valoare in rez.items():
        if isinstance(valoare, list):
            if len(valoare) > 0 and isinstance(valoare[0], tuple):
                rez[key] = ", ".join([f"{r[0]} {r[1]} {r[2]}" for r in valoare])
            else:
                rez[key] = ", ".join(str(v) for v in valoare)
                
    write_header = not os.path.exists(fisier_exp_csv) or os.path.getsize(fisier_exp_csv) == 0
                
    with open(fisier_exp_csv, mode='a', newline='', encoding='utf-8') as f_csv:
        writer = csv.writer(f_csv)
        if write_header:
            writer.writerow(rez.keys())
        writer.writerow(rez.values())
        
    print(f"\n Raportul  salvat in: 'raport_evaluare.txt'")
    print(f"Datele au fost salvate in: 'rezultate2.csv'\n")

if __name__ == "__main__":
    main()