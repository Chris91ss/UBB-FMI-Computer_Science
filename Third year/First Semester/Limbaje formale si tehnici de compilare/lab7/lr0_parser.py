"""
LR(0) parser for the mini DSL (lab7).
Conflicts are resolved by preferring shift over reduce (standard approach).
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

import importlib.util
spec_lab5 = importlib.util.spec_from_file_location(
    "lab5_scanner", REPO_ROOT / "lab5" / "scanner.py"
)
lab5_module = importlib.util.module_from_spec(spec_lab5)
spec_lab5.loader.exec_module(lab5_module)
Lab5Lexer = lab5_module.Lexer

EPSILON = "eps"  # how we show an empty right-hand side
ENDMARK = "$"    # special end-of-input marker


@dataclass(frozen=True)
class Production:
    """One grammar rule: lhs -> rhs."""
    lhs: str
    rhs: Tuple[str, ...]

    def rhs_pretty(self) -> str:
        """Right-hand side as a simple string (or eps if empty)."""
        return " ".join(self.rhs) if self.rhs else EPSILON


@dataclass(frozen=True)
class LR0Item:
    """A production with a dot showing how much we already matched."""
    lhs: str
    rhs: Tuple[str, ...]
    dot: int

    def next_symbol(self) -> Optional[str]:
        """Symbol after the dot, or None if the dot is at the end."""
        return self.rhs[self.dot] if self.dot < len(self.rhs) else None

    def advance(self) -> "LR0Item":
        """Return a new item where the dot moved one step to the right."""
        return LR0Item(self.lhs, self.rhs, self.dot + 1)


class Grammar:
    def __init__(self, productions: List[Production], start: str):
        """Holds all productions for a grammar and some helper sets/maps."""
        self.productions = productions
        self.start = start
        self.nonterminals: Set[str] = {p.lhs for p in productions}
        all_rhs = {sym for p in productions for sym in p.rhs}
        self.terminals: Set[str] = all_rhs - self.nonterminals - {EPSILON}
        self.by_lhs: Dict[str, List[Production]] = {}
        for p in productions:
            self.by_lhs.setdefault(p.lhs, []).append(p)

    @classmethod
    def from_file(cls, path: Path) -> "Grammar":
        """Load a grammar from a text file with rules like `S -> A B | a`."""
        prods: List[Production] = []
        start: Optional[str] = None
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                lhs_part, rhs_part = line.split("->")
                lhs = lhs_part.strip()
                if start is None:
                    start = lhs
                for alt in rhs_part.split("|"):
                    symbols = [s for s in alt.strip().split() if s]
                    if symbols in ([EPSILON], ["eps"], ["ε"]):
                        symbols = []
                    prods.append(Production(lhs, tuple(symbols)))
        if start is None:
            raise ValueError("Grammar file is empty.")
        return cls(prods, start)

    def augmented(self) -> "Grammar":
        """Add a new start rule S' -> S, needed for LR parsing."""
        aug_start = f"{self.start}'"
        aug_prod = Production(aug_start, (self.start,))
        return Grammar([aug_prod] + self.productions, aug_start)


def closure(items: Iterable[LR0Item], grammar: Grammar) -> List[LR0Item]:
    """Compute LR(0) closure: expand items when the dot is before a nonterminal."""
    result = list(items)  # start with the given items
    changed = True        # keep going while we keep adding new items
    while changed:
        changed = False
        for it in list(result):
            sym = it.next_symbol()  # symbol after the dot
            if sym and sym in grammar.nonterminals:  # only expand nonterminals
                for prod in grammar.by_lhs.get(sym, []):  # all rules for that nonterminal
                    new_item = LR0Item(prod.lhs, prod.rhs, 0)  # dot at the start
                    if new_item not in result:  # avoid duplicates
                        result.append(new_item)  # add new item
                        changed = True          # we grew the set, so repeat
    return result


def goto(items: Iterable[LR0Item], symbol: str, grammar: Grammar) -> List[LR0Item]:
    """Compute LR(0) goto: move the dot over `symbol` and take closure."""
    # Move the dot over `symbol` in all items where the next symbol matches.
    advanced = [it.advance() for it in items if it.next_symbol() == symbol]
    # Then take closure to include any new items introduced by nonterminals.
    return closure(advanced, grammar)


class LR0Parser:
    def __init__(self, grammar: Grammar):
        """Build LR(0) states and ACTION/GOTO tables from the given grammar."""
        self.grammar = grammar.augmented()  # use augmented grammar with new start S'
        self.states: List[List[LR0Item]] = []  # list of LR(0) item sets (states)
        self.action: Dict[Tuple[int, str], Tuple[str, int]] = {}  # ACTION table
        self.goto_table: Dict[Tuple[int, str], int] = {}  # GOTO table
        self.conflicts: List[str] = []  # store info about LR(0) conflicts
        self._build_automaton()  # build states and goto_table
        self._build_tables()     # fill ACTION table

    def _build_automaton(self) -> None:
        """Build all LR(0) states (sets of items) and the raw goto transitions."""
        # Initial item: S' -> . S  (dot at the start of the original start symbol)
        start_item = LR0Item(
            self.grammar.start,
            self.grammar.by_lhs[self.grammar.start][0].rhs,
            0
        )
        # First state is the closure of that item.
        self.states.append(closure([start_item], self.grammar))
        changed = True  # we will add states until no more are found
        while changed:
            changed = False
            for idx, state in list(enumerate(self.states)):
                # All symbols that appear after the dot in this state.
                symbols = {it.next_symbol() for it in state if it.next_symbol()}
                for sym in symbols:
                    target = goto(state, sym, self.grammar)  # next state on `sym`
                    if not target:  # empty set => no transition
                        continue
                    if target not in self.states:  # new state discovered
                        self.states.append(target)  # add it
                        target_idx = len(self.states) - 1  # its index
                        changed = True  # we extended the list, so loop again
                    else:
                        target_idx = self.states.index(target)  # already known
                    # Record DFA transition: from state `idx` on symbol `sym` to `target_idx`.
                    self.goto_table[(idx, sym)] = target_idx

    def _add_action(self, state: int, terminal: str, action: Tuple[str, int]) -> None:
        """Insert an entry into ACTION, handling and recording conflicts."""
        key = (state, terminal)
        if key in self.action:  # there is already an action for this cell
            old = self.action[key]
            if old != action:  # true conflict (two different actions)
                # Prefer shift over reduce in shift/reduce conflicts.
                if old[0] == "shift" and action[0] == "reduce":
                    return  # keep existing shift
                if old[0] == "reduce" and action[0] == "shift":
                    self.action[key] = action  # overwrite reduce with shift
                    self.conflicts.append(
                        f"Shift/reduce at state {state} on '{terminal}' (shift chosen)"
                    )
                    return
                # Other conflicts are just recorded.
                self.conflicts.append(
                    f"Conflict at state {state} on '{terminal}': {old} vs {action}"
                )
        # Normal case: no conflict or we decided to overwrite.
        self.action[key] = action

    def _build_tables(self) -> None:
        """Fill the ACTION table (shift/reduce/accept) using the LR(0) states."""
        for idx, state in enumerate(self.states):
            for item in state:
                sym = item.next_symbol()  # symbol after the dot
                if sym is None:  # dot at the end: candidate for reduce / accept
                    if item.lhs == self.grammar.start:
                        # S' -> S .   on end marker: accept
                        self._add_action(idx, ENDMARK, ("accept", 0))
                    else:
                        # A -> α .   on any terminal or end marker: reduce
                        prod_idx = self._prod_index(item.lhs, item.rhs)
                        for t in self.grammar.terminals | {ENDMARK}:
                            self._add_action(idx, t, ("reduce", prod_idx))
                elif sym in self.grammar.terminals:
                    # Dot before a terminal: if goto gives a state, we do a shift.
                    target = self.goto_table.get((idx, sym))
                    if target is not None:
                        self._add_action(idx, sym, ("shift", target))

    def _prod_index(self, lhs: str, rhs: Tuple[str, ...]) -> int:
        """Find the index of production `lhs -> rhs` inside the augmented grammar."""
        for i, p in enumerate(self.grammar.productions):
            if p.lhs == lhs and p.rhs == rhs:
                return i
        raise ValueError("Production not found")

    @dataclass
    class Node:
        """One node in the parse tree (id, symbol, and its children IDs)."""
        id: int
        symbol: str
        children: List[int]

    def parse(self, tokens: Sequence[str]) -> Tuple[List[str], List[Tuple[int, str, int, int]]]:
        """Run the LR(0) parser on a list of token names and build a parse tree."""
        stack = [0]  # stack of parser states, starts in state 0
        node_stack: List[int] = []  # stack of node IDs for building the tree
        nodes: Dict[int, LR0Parser.Node] = {}  # id -> Node
        next_id = 0  # next free node id
        prod_log: List[str] = []  # sequence of reductions (unused by caller now)
        i = 0  # index in the input stream
        stream = list(tokens) + [ENDMARK]  # add end marker at the end

        while True:
            state = stack[-1]            # current state (top of stack)
            a = stream[i]                # current input symbol
            action = self.action.get((state, a))  # lookup in ACTION table
            if action is None:
                raise SyntaxError(f"Unexpected '{a}' at position {i} (state {state})")

            kind, value = action
            if kind == "shift":
                # Shift: push new state and create a leaf node for the terminal.
                stack.append(value)
                nodes[next_id] = LR0Parser.Node(next_id, a, [])
                node_stack.append(next_id)
                next_id += 1
                i += 1  # consume one input symbol
            elif kind == "reduce":
                # Reduce by production A -> rhs.
                prod = self.grammar.productions[value]
                rhs_len = len(prod.rhs)
                children = []
                if rhs_len:
                    # Pop as many states / nodes as symbols on the right-hand side.
                    stack = stack[:-rhs_len]
                    children = node_stack[-rhs_len:]
                    node_stack = node_stack[:-rhs_len]
                # After reduction, go to the state from top of stack on nonterminal A.
                goto_state = self.goto_table.get((stack[-1], prod.lhs))
                if goto_state is None:
                    raise SyntaxError(f"No goto for {prod.lhs} from state {stack[-1]}")
                stack.append(goto_state)
                # Create a new node for A with the collected children.
                nodes[next_id] = LR0Parser.Node(next_id, prod.lhs, children)
                node_stack.append(next_id)
                next_id += 1
                prod_log.append(f"{prod.lhs} -> {prod.rhs_pretty()}")
            elif kind == "accept":
                # Input fully recognized.
                break

        # The last node on the node stack is the root of the parse tree.
        root_id = node_stack[-1] if node_stack else -1
        return prod_log, self._father_sibling(nodes, root_id)

    def _father_sibling(self, nodes: Dict[int, Node], root: int) -> List[Tuple[int, str, int, int]]:
        """Turn the tree into (id, symbol, parent_id, sibling_id) rows."""
        rows: List[Tuple[int, str, int, int]] = []  # final table rows

        def walk(nid: int):
            """Depth-first traversal that fills `rows` for all children."""
            node = nodes[nid]
            for idx, cid in enumerate(node.children):
                # Next sibling is the child to the right, or -1 if last child.
                sib = node.children[idx + 1] if idx + 1 < len(node.children) else -1
                rows.append((cid, nodes[cid].symbol, nid, sib))
                walk(cid)  # recurse into the child

        if root != -1:
            # Root has no parent and no sibling.
            rows.append((root, nodes[root].symbol, -1, -1))
            walk(root)
        return rows


# ---------- Full Mini-DSL Grammar ----------

def load_minidsl_grammar() -> Grammar:
    """Full grammar to parse lab2/program1.txt"""
    prods = [
        # Program structure
        Production("Program", ("QuestBlock", "WhenBlocks", "OptIf")),

        # Quest block
        Production("QuestBlock", ("QUEST", "STRING", "LBRACE", "QuestBody", "RBRACE")),
        Production("QuestBody", ("RequiresSec", "ObjectivesSec", "RewardsSec", "HookSecs")),

        # Requires
        Production("RequiresSec", ("REQUIRES", "Expr")),

        # Objectives
        Production("ObjectivesSec", ("OBJECTIVES", "COLON", "ObjList")),
        Production("ObjList", ("Obj",)),
        Production("ObjList", ("ObjList", "COMMA", "Obj")),
        Production("Obj", ("GO_TO", "STRING")),
        Production("Obj", ("TALK_TO", "STRING")),
        Production("Obj", ("COLLECT", "STRING", "COUNT", "NUMBER")),
        Production("Obj", ("DEFEAT", "STRING", "COUNT", "NUMBER")),
        Production("Obj", ("INTERACT", "STRING")),
        Production("Obj", ("CUSTOM", "STRING")),

        # Rewards
        Production("RewardsSec", ("REWARDS", "COLON", "RewList")),
        Production("RewList", ("Rew",)),
        Production("RewList", ("RewList", "COMMA", "Rew")),
        Production("Rew", ("XP", "NUMBER")),
        Production("Rew", ("GOLD", "NUMBER")),
        Production("Rew", ("ITEM", "STRING")),
        Production("Rew", ("ITEM", "STRING", "COUNT", "NUMBER")),
        Production("Rew", ("UNLOCK", "STRING")),

        # Hooks
        Production("HookSecs", ("Hook",)),
        Production("HookSecs", ("HookSecs", "Hook")),
        Production("Hook", ("ON_ACCEPT", "COLON", "Stmts", "END")),
        Production("Hook", ("ON_COMPLETE", "COLON", "Stmts", "END")),
        Production("Hook", ("ON_UPDATE", "COLON", "Stmts", "END")),

        # When blocks
        Production("WhenBlocks", ()),  # epsilon
        Production("WhenBlocks", ("WhenBlocks", "WhenBlock")),
        Production("WhenBlock", ("WHEN", "Event", "COLON", "Stmts", "END")),
        Production("Event", ("ENTER", "STRING")),
        Production("Event", ("TALK", "STRING")),
        Production("Event", ("PICKUP", "STRING")),
        Production("Event", ("KILL", "STRING")),

        # Optional trailing if
        Production("OptIf", ()),  # epsilon
        Production("OptIf", ("IF", "Expr", "COLON", "Stmts", "END")),

        # Statements
        Production("Stmts", ("Stmt",)),
        Production("Stmts", ("Stmts", "Stmt")),
        Production("Stmt", ("PRINT", "STRING")),
        Production("Stmt", ("SET", "IDENT", "ASSIGN", "Expr")),
        Production("Stmt", ("GIVE", "XP", "NUMBER")),
        Production("Stmt", ("UNLOCK", "STRING")),
        Production("Stmt", ("IF", "Expr", "COLON", "Stmts", "END")),

        # Expressions
        Production("Expr", ("Expr", "AND", "Expr")),
        Production("Expr", ("Expr", "OR", "Expr")),
        Production("Expr", ("NOT", "Expr")),
        Production("Expr", ("Expr", "EQ", "Expr")),
        Production("Expr", ("LPAREN", "Expr", "RPAREN")),
        Production("Expr", ("Atom",)),
        Production("Expr", ("FuncCall",)),

        # Atoms
        Production("Atom", ("IDENT",)),
        Production("Atom", ("STRING",)),
        Production("Atom", ("NUMBER",)),
        Production("Atom", ("TRUE",)),
        Production("Atom", ("FALSE",)),

        # Function calls
        Production("FuncCall", ("IDENT", "LPAREN", "RPAREN")),
        Production("FuncCall", ("IDENT", "LPAREN", "ArgList", "RPAREN")),
        Production("ArgList", ("Arg",)),
        Production("ArgList", ("ArgList", "COMMA", "Arg")),
        Production("Arg", ("STRING",)),
        Production("Arg", ("NUMBER",)),
        Production("Arg", ("IDENT",)),
    ]
    return Grammar(prods, "Program")


def pif_to_tokens(pif_rows: List[Dict]) -> List[str]:
    """Map Lab5 PIF to terminal names."""
    tokens = []
    for row in pif_rows:
        typ = row["type"]
        lex = row["lexeme"]

        if typ == "KEYWORD":
            tokens.append(lex.upper())
        elif typ == "LOGICAL":
            tokens.append(lex.upper())
        elif typ == "SEP":
            m = {"{": "LBRACE", "}": "RBRACE", "(": "LPAREN", ")": "RPAREN", ":": "COLON", ",": "COMMA"}
            tokens.append(m[lex])
        elif typ == "OP":
            m = {"=": "ASSIGN", "==": "EQ", "!=": "NE", "<": "LT", ">": "GT", "<=": "LE", ">=": "GE"}
            tokens.append(m.get(lex, lex))
        elif typ == "CONST_OR_IDENT":
            if lex.startswith('"'):
                tokens.append("STRING")
            elif lex.isdigit() or (lex[0] == '-' and lex[1:].isdigit()):
                tokens.append("NUMBER")
            elif lex in ("true", "false"):
                tokens.append(lex.upper())
            else:
                tokens.append("IDENT")
        else:
            raise ValueError(f"Unknown PIF type: {typ}")
    return tokens


# ---------- CLI ----------

def run_manual(grammar_path: Path, sequence: List[str]) -> None:
    grammar = Grammar.from_file(grammar_path)
    parser = LR0Parser(grammar)
    try:
        _prods, table = parser.parse(sequence)
    except SyntaxError as e:
        print(f"Parsing failed: {e}")
        return
    print("\nFather/Sibling table (id, symbol, parent, sibling):")
    for row in table:
        print(row)


def run_minidsl(source_path: Path) -> None:
    scanner = Lab5Lexer()
    out = scanner.run(str(source_path))
    if out["errors"]:
        print("Lexical errors:")
        for e in out["errors"]:
            print(f"  {e}")
        return

    tokens = pif_to_tokens(out["pif"])
    grammar = load_minidsl_grammar()
    parser = LR0Parser(grammar)

    try:
        _prods, table = parser.parse(tokens)
    except SyntaxError as e:
        print(f"Parsing failed: {e}")
        return

    print("\nFather/Sibling table (id, symbol, parent, sibling):")
    for row in table:
        print(row)


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="LR(0) parser (lab7)")
    sub = ap.add_subparsers(dest="mode", required=True)

    manual = sub.add_parser("manual", help="Parse with grammar file")
    manual.add_argument("--grammar", required=True, type=Path)
    manual.add_argument("--sequence", required=True)

    mini = sub.add_parser("minidsl", help="Parse DSL source using Lab5 scanner")
    mini.add_argument("source", type=Path)

    args = ap.parse_args(argv)
    if args.mode == "manual":
        run_manual(args.grammar, args.sequence.split())
    else:
        run_minidsl(args.source)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
