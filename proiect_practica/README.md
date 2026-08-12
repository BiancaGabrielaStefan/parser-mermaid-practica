# Evaluarea Capacității Asistenților AI de a Genera Arhitecturi Software (UML)

## Structură Repo
 * `parser_mermaid.py` - Scriptul principal dezvoltat în Python. Folosește Expresii Regulate (Regex) pentru a parsa codul Mermaid și a contoriza elementele OOP.
 * `cod_mermaid.txt` - Fișierul de input în care se introduce codul diagramei ce urmează a fi analizată.
 * `rezultate.csv` - Fișierul de output generat de script, conținând datele extrase (actualizat prin *append* la fiecare rulare).
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

### 2. Funcția `main`
* **Conversia datelor structurate:** Listele și tuplurile extrase de Regex sunt parcurse și transformate în string-uri separate prin virgulă folosind metoda `.join()`, pentru a preveni erorile de formatare în Excel
* **Append Mode:** Scriptul verifică dacă fișierul `rezultate.csv` există sau este gol (`os.path.getsize`). Dacă este un test nou, generează dinamic capul de tabel (`writer.writerow(rez.keys())`). Apoi, adaugă rezultatele noii rulări pe un rând nou (`mode='a'`), iar astfel permite rularea testelor succesive fără a pierde datele anterioare

## Utilizare

Pentru a putea fi rulat local parser-ul, e necesar Python 3.x (programul a fost dezvoltat si testat pe versiunea Python 3.14.6).
Clonare repository: