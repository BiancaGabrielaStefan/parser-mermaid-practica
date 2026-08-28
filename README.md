# Evaluarea Capacității Asistenților AI de a Genera Arhitecturi Software (UML)

## Structură Repo
* `cod_mermaid.txt` - Fișierul de input în care se introduce codul diagramei ce urmează a fi analizată.

**Versiunea 1 (Inițială):**
* `parser_mermaid.py` - Scriptul de bază care extrage clasele, atributele, metodele și relațiile.
* `rezultate.csv` - Fișierul de output generat de prima versiune a scriptului.

**Versiunea 2 (Îmbunătățită):**
* `parser2.py` - Versiunea actualizată a parserului, care include detectarea claselor abstracte și filtre avansate.
* `rezultate2.csv` - Noul fișier tabelar generat de V2, cu formatarea relațiilor ajustată pentru Excel.
* `raport_evaluare.txt` - Fișier nou, generat de V2, care oferă o vizualizare text clară și ușor de citit (human-readable) a elementelor extrase.
* Domeniile testate (pe 3 niveluri de complexitate a prompturilor):
  1. *Platformă de E-Learning*
  2. *Sistem de gestiune a unei farmacii*

## Implementare

### 1. Funcția `mermaid_parser`
Scriptul verifică mai întâi dacă fișierul conține declarația `classDiagram`, apoi extrage următoarele entități:
* **Clasele:** Caută pattern-ul `class NumeClasa {` pentru a contoriza și lista entitățile definite
* **Atributele vs Metodele:** Pentru a face diferența între atribute și metode, scriptul folosește flag-ul `re.MULTILINE` 
  * *Atributele* sunt identificate prin simbolurile de vizibilitate (`+`, `-`, `#`, `~`) și lipsa parantezelor
  * *Metodele* sunt extrase căutând paranteze `()`
* **Clasificarea relațiilor:** Scriptul folosește un Regex complex pentru a capta relațiile sub formă de tupluri: `(Sursă, Tip_Săgeată, Destinație)`. Ulterior, un algoritm de decizie (`if/elif`) clasifică săgețile în 3 categorii specifice conceptelor de OOP:
  * *Moșteniri:* `<|--` sau `--|>`
  * *Compoziții:* `*--` sau `--*`
  * *Asocieri simple:* `-->`, `<--` sau `--`

  ### 2. Îmbunătățiri în V2 (`mermaid_parser2`)
Pentru a rezolva limitările primei versiuni, au fost adăugate următoarele funcționalități:
* **Detectarea claselor abstracte:** Implementarea căutării etichetei `<<abstract>>`. Scriptul adaugă automat sufixul `(Abstract)` la numele clasei, verificând astfel aplicarea corectă a polimorfismului.
* **Filtrarea atributelor:** Regex-ul a fost rafinat (`^[ \t\xa0]*...`) pentru a ignora automat liniile goale și caracterele de tip *non-breaking space*.
* **Formatare sigură pentru Excel:** S-a modificat sintaxa de ieșire pentru tipurile de relații din formatul cu slash (`X / Y / Z`) în formatul: (`A:X | C:Y | M:Z`). Această ajustare previne comportamentul de auto-formatare al aplicației, care convertea eronat datele extrase în date calendaristice.

### 3. Funcția `main`
* **Conversia datelor structurate:** Listele și tuplurile extrase de Regex sunt parcurse și transformate în string-uri separate prin virgulă folosind metoda `.join()`, pentru a preveni erorile de formatare în Excel
* **Append Mode:** Scriptul verifică dacă fișierul `rezultate.csv` există sau este gol (`os.path.getsize`). Dacă este un test nou, generează dinamic capul de tabel (`writer.writerow(rez.keys())`). Apoi, adaugă rezultatele noii rulări pe un rând nou (`mode='a'`), iar astfel permite rularea testelor succesive fără a pierde datele anterioare

## Utilizare

Pentru a putea fi rulat local parser-ul, e necesar Python 3.x (programul a fost dezvoltat si testat pe versiunea Python 3.14.6).
Clonare repository:
```bash
   git clone https://github.com/BiancaGabrielaStefan/parser-mermaid-practica.git
```
