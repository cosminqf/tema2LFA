# Tema 2 LFA

## Descriere

Acest proiect implementează un lanț complet de procesare a unei expresii regulate, cu următorii pași:

1. **Transformarea expresiei regulate într-o formă postfixată (notatie poloneză inversă).**
2. **Construirea unui NFA folosind algoritmul Thompson.**
3. **Conversia NFA-ului într-un DFA (automat determinist finit).**
4. **Verificarea unor șiruri de test dacă sunt acceptate de DFA-ul rezultat.**

## Structura

- `tema2.py` – conține tot codul principal:
  - `regex_to_postfix(regex)` – transformă o expresie în formă postfixată.
  - `thompson(forma_postfix)` – construiește un NFA folosind algoritmul Thompson.
  - `convert_nfa_to_dfa(nfa)` – transformă NFA-ul în DFA.
  - `acceptare_dfa(dfa, line)` – verifică dacă un șir este acceptat de DFA.
  - `verify()` – încarcă fișierul `tests.json` și rulează toate testele.

- `tests.json` – fișier JSON care conține o listă de teste cu următoarea structură:
  ```json
  [
    {
      "name": "R1",
      "regex": "a*b",
      "test_strings": [
        {"input": "b", "expected": true},
        {"input": "aaab", "expected": true},
        {"input": "ab", "expected": true},
        {"input": "a", "expected": false}
      ]
    }
  ]
  ```

## Rulare cod

Asigură-te că ai Python instalat (versiunea 3.6+ recomandată).

1. Plasează fișierul `tema2.py` și `tests.json` în același director.
2. Deschide un terminal/command prompt în acel director.
3. Rulează:
   ```bash
   python tema2.py
   ```
4. Vei vedea rezultatele testelor în consolă, împreună cu mesajele "PASS" sau "FAIL".

## Decizii de implementare

- **Expresia postfixată** este generată pentru a simplifica implementarea algoritmului Thompson.
- **Algoritmul Thompson** este utilizat pentru construirea pas cu pas a unui NFA pentru fiecare simbol și operator.
- **În NFA**, tranzițiile lambda sunt păstrate în câmpul `eps`, separat de tranzițiile normale.
- **În conversia către DFA**, se folosește închideri epsilon și gruparea stărilor NFA într-o singură stare DFA (subset construction).
- **DFA-ul rezultat** este folosit pentru testarea fiecărui șir de intrare dat în `tests.json`.

## Culori în consolă

- ✅ Verde pentru testele trecute (PASS)
- ❌ Roșu pentru testele eșuate (FAIL)
- Aceste culori apar în terminalele care suportă ANSI (Linux, Mac, unele terminale Windows)

## Exemple de rulare

```bash
Rezultate test R1 cu regex a|b :
Pentru string-ul a trebuia sa obtinem True si am obtinut True -> ✅ PASS
Pentru string-ul ab trebuia sa obtinem False si am obtinut False -> ✅ PASS
```

---

Proiect realizat pentru cursul de **Limbaje Formale și Automate** din cadrul **Facultatii de Matematica si Informatica - Universitatea din Bucuresti**.
