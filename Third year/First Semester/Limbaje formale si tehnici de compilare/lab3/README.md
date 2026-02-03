Game Quests DSL — Lexical Analyzer (Lab 3)

Quick Start
===========

Run these 2 commands from the repo root:

```bash
# Program 1
python lab3/lexer.py lab2/program1.txt --out lab3/out_prog1

# Program 2
python lab3/lexer.py lab2/program2.txt --out lab3/out_prog2
```

Output Files
============

Each command creates 3 files:

- `<out>_pif.txt` — Program Internal Form (token + symbol table location)
- `<out>_st.txt` — Symbol Table (bucket/position → lexeme)
- `<out>_errors.txt` — Lexical errors (if any)

What it recognizes
==================

- **Keywords**: quest, requires, objectives, rewards, on_accept, on_update, on_complete, npc, item, location, dialog, line, go_to, talk_to, collect, defeat, interact, custom, set, give, take, spawn, at, unlock, print, if, while, for, in, end, when, enter, talk, pickup, kill, timer, quest_state, xp, gold, flag, count
- **Booleans**: true, false (stored in ST)
- **Operators**: ==, !=, <=, >=, =, <, >, ..
- **Separators**: { } ( ) , : ;
- **Identifiers**: [A-Za-z][A-Za-z0-9_]*
- **Numbers**: 0 | [1-9][0-9]*
- **Strings**: "..." (no newlines)
- **Comments**: # to end of line

Symbol Table Implementation
===========================

- **Hash table with separate chaining**: Fixed array of buckets (lists) with a polynomial rolling hash; collisions are stored in the same bucket.
