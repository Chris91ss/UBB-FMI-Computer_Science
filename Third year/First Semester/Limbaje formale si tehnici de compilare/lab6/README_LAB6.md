Lab 6 — Parser for the Mini DSL
--------------------------------

Overview
--------
- Scanner + Parser: `lab6/parser.py` now reuses the Lab 5 scanner to build the Program Internal Form (PIF), then feeds those tokens into a PLY (Python Lex‑Yacc) parser.
- FA reuse: identifier and number validation continues to happen inside the Lab 5 scanner via the Lab 4 DFAs.
- Grammar: same subset of the DSL as previous labs (quests, objectives, rewards, hooks, when-blocks, statements).
- Output: after a successful parse, we print the ordered list of productions; syntax errors are reported with token info.
- Dependency: install PLY once via `pip install ply` (required before running the parser).

Setup
-----
```bash
pip install ply
```
- Output: prints the sequence of productions (grammar rules) used during parsing, or reports syntax errors.

Grammar (subset of DSL)
-----------------------
Non-terminals (main):
- program → quest_block when_list opt_if
- quest_block → QUEST STRING LBRACE quest_body RBRACE
- quest_body → requires_section objectives_section rewards_section hook_sections
- requires_section → REQUIRES expression
- objectives_section → OBJECTIVES COLON objective_list
- rewards_section → REWARDS COLON reward_list
- hook_sections → hook_sections hook | hook
- when_list → when_list when_block | ε
- when_block → WHEN event COLON statements END
- statements → statements statement | statement
- statement → PRINT STRING | SET IDENT ASSIGN literal | GIVE XP NUMBER | UNLOCK STRING | IF condition COLON statements END
- condition / expression → standard boolean/relational expressions with AND/OR/NOT and comparisons (=, !=, <=, >=, <, >)
- objective → GO_TO STRING | TALK_TO STRING | COLLECT STRING COUNT NUMBER | DEFEAT STRING COUNT NUMBER | INTERACT STRING | CUSTOM STRING
- reward → XP NUMBER | GOLD NUMBER | ITEM STRING (COUNT NUMBER)?

Tokens and integration
----------------------
- `lab5/scanner.py` produces the PIF/St/errors triple. The parser aborts early if the scanner reports lexical errors so we keep Lab 3/4 behavior intact.
- Each PIF row is mapped back into the PLY tokens defined in `parser.py`, so the grammar still sees `QUEST`, `GO_TO`, `STRING`, `NUMBER`, `BOOLEAN`, `IDENT`, etc.
- Function calls inside expressions (`level_at_least(2)`, `completed("Quest")`, `in_location(...)`, etc.) are still parsed via `expression -> IDENT LPAREN argument_list RPAREN`.

Run
---
```bash
# Parses lab2/program1.txt and prints production sequence
python lab6/parser.py lab2/program1.txt
```

Expected output
---------------
- If parsing succeeds: “Parsing succeeded. Production sequence:” followed by grammar rule names for each reduction.
- If scanning or parsing fails: errors are shown (scanner errors first, then syntax errors).

Notes
-----
- This parser handles a simplified subset of the DSL sufficient for the sample programs (`program1.txt`), focusing on quests, when-blocks, and control statements inside hooks.
- Running `parser.py` first calls the Lab 5 scanner (FA-powered), then streams those tokens into the PLY parser, so we explicitly show the pipeline “PIF → parser”.
- The production log you see after a successful parse is the same as before; it now just includes every converted PIF token before the grammar reductions.




