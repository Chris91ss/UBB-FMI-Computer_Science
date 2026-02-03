# Lab 7 — LR(0) Parsing

LR(0) parser implementation that parses the full mini DSL from lab2.

## Requirements Covered

| Requirement                                                       |  |
| ----------------------------------------------------------------- | - |
| 1. Implement LR(0) with seminar grammar + sequence → productions |  |
| 2.a. Productions string                                           |  |
| 2.b. Derivations string                                           |  |
| 2.c. Father/sibling table                                         |  |

## Files

- `lr0_parser.py` — LR(0) parser implementation
- `grammar_seminar.txt` — simple grammar for Requirement 1

## Usage

### Requirement 1: Manual grammar + sequence

```
python lab7/lr0_parser.py manual --grammar lab7/grammar_seminar.txt --sequence "a b"
```

### Requirement 2: Mini DSL + PIF (uses Lab5 scanner)

```
python lab7/lr0_parser.py minidsl lab2/program1.txt
```

## Grammar

### Seminar grammar (grammar_seminar.txt)

```
S -> A B
A -> a
B -> b
```

### Mini DSL grammar (built-in)

Covers: quest blocks, requires, objectives, rewards, hooks, when blocks, if statements, expressions with function calls, logical operators (and/or/not), comparison (==).

```
Program -> QuestBlock WhenBlocks OptIf
QuestBlock -> QUEST STRING LBRACE QuestBody RBRACE
QuestBody -> RequiresSec ObjectivesSec RewardsSec HookSecs
RequiresSec -> REQUIRES Expr
ObjectivesSec -> OBJECTIVES COLON ObjList
ObjList -> Obj | ObjList COMMA Obj
Obj -> GO_TO STRING | TALK_TO STRING | COLLECT STRING COUNT NUMBER | ...
RewardsSec -> REWARDS COLON RewList
RewList -> Rew | RewList COMMA Rew
Rew -> XP NUMBER | GOLD NUMBER | ITEM STRING | ITEM STRING COUNT NUMBER
HookSecs -> Hook | HookSecs Hook
Hook -> ON_ACCEPT COLON Stmts END | ON_COMPLETE COLON Stmts END
WhenBlocks -> eps | WhenBlocks WhenBlock
WhenBlock -> WHEN Event COLON Stmts END
Event -> ENTER STRING | TALK STRING | PICKUP STRING | KILL STRING
OptIf -> eps | IF Expr COLON Stmts END
Stmts -> Stmt | Stmts Stmt
Stmt -> PRINT STRING | SET IDENT ASSIGN Expr | GIVE XP NUMBER | IF Expr COLON Stmts END
Expr -> Expr AND Expr | Expr OR Expr | NOT Expr | Expr EQ Expr | Atom | FuncCall
Atom -> IDENT | STRING | NUMBER | TRUE | FALSE
FuncCall -> IDENT LPAREN ArgList RPAREN | IDENT LPAREN RPAREN
ArgList -> Arg | ArgList COMMA Arg
Arg -> STRING | NUMBER | IDENT
```

## Output

1. **Productions** — sequence of reductions used during parsing
2. **Father/Sibling table** — parse tree as `(node_id, symbol, parent_id, sibling_id)`
   - `parent_id = -1` means root
   - `sibling_id = -1` means no right sibling

## LR(0) Conflicts

LR(0) is strict and produces shift/reduce conflicts for most real grammars. These are resolved by **preferring shift** (standard approach used by YACC/Bison).

## Example Output

```
$ python lab7/lr0_parser.py minidsl lab2/program1.txt

LR(0) conflicts (27 resolved by preferring shift):
  Shift/reduce at state 5 on 'IF' (shift chosen)
  ...

Productions:
Arg -> NUMBER
ArgList -> Arg
FuncCall -> IDENT LPAREN ArgList RPAREN
Expr -> FuncCall
...
Program -> QuestBlock WhenBlocks OptIf

Father/Sibling table (id, symbol, parent, sibling):
(212, 'Program', -1, -1)
(103, 'QuestBlock', 212, 183)
...
```
