Lab 5 — Scanner with FA Integration
-----------------------------------

What this scanner does
- Reuses the Lab 3 tokenization pipeline (keywords, operators, separators, strings, comments).
- Validates identifiers and integer constants using the finite automata defined in Lab 4 (`lab4/fa_identifier.json`, `lab4/fa_number.json`).
- Keeps the symbol table (hash-table buckets) and PIF formats unchanged.

How identifier/constant validation works
- On each candidate identifier, the scanner runs the identifier FA. If it rejects, the token is reported as an invalid identifier.
- On each candidate number (sequence of digits), the scanner runs the number FA. If it rejects, the token is reported as an invalid number.
- Keywords/logical words (`and`, `or`, `not`) are still recognized separately after FA acceptance.

Run

```bash
# Validate a source file and write outputs next to it
python lab5/scanner.py lab2/program1.txt --out lab5/out_program1

# Quick run with console output only
python lab5/scanner.py lab2/program1.txt
```

Outputs
- `_pif.txt`: `#  TYPE  LEXEME  BUCKET  POS`
- `_st.txt`: `BUCKET  POS  LEXEME`
- `_errors.txt`: any lexical errors, or “No lexical errors.”

Dependencies
- Uses `lab3.symbol_table.SymbolTable`.
- Loads FA JSONs from `lab4/`.


