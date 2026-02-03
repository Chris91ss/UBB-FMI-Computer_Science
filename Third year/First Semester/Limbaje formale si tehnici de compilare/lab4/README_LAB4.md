Lab 4 — Finite Automata (FA) and Regular Grammar (RG) Toolkit

What this does
--------------
- Define FAs in JSON, validate strings, pretty-print
- Convert FA (identifier/number) to an equivalent right-linear grammar (FA → RG)
- Load FAs from JSON and print grammars directly (no external grammar files)

JSON schema
-----------
{
  "states": ["q0", "q1"],
  "alphabet": ["a", "b", "0", "1", "_"],
  "start_state": "q0",
  "final_states": ["q1"],
  "transitions": [
    { "from": "q0", "symbol": "a", "to": "q1" },
    { "from": "q1", "symbol": "b", "to": "q1" },
    { "from": "q1", "symbol": "ε", "to": "q0" }
  ]
}
Notes: use "ε" for epsilon; DFA transitions are total, NFA may be non-total.

Commands (from repo root)
-------------------------
One-command demo (recommended):
```bash
python lab4/fa_rg_transformation.py demo
```

Validate input against FA (handwritten JSONs):
```bash
python lab4/fa_rg_transformation.py accept --fa lab4/fa_identifier.json --input foo_bar9
```

Pretty-print FA:
```bash
python lab4/fa_rg_transformation.py show --fa lab4/fa_number.json
```

Convert FA → RG (right-linear) and print productions:
```bash
python lab4/fa_rg_transformation.py fa2rg --fa lab4/fa_identifier.json
python lab4/fa_rg_transformation.py fa2rg --fa lab4/fa_number.json
```

FA → RG format
--------------
- One nonterminal per FA state (state name used as nonterminal)
- For each transition q -a-> p, add production: q -> a p
- For each final state f, add production: f -> ε
- Start nonterminal = FA start_state

- `lab4/fa_identifier.json`: identifiers start with letter/_ then letter/digit/_ (lowercase a–z + _ + digits)
- `lab4/fa_number.json`: integers (one or more digits)

Assumptions & limits
--------------------
- Terminals are single characters (digits, letters, underscore)
- Grammars printed are right-linear and derived from the current FA JSONs
- No external packages; outputs are deterministic and pretty-printed


