import json
import sys
import argparse
from typing import Dict, Set, List, Tuple


EPSILON = "ε"


class FiniteAutomaton:
    def __init__(self,
                 states: Set[str],
                 alphabet: Set[str],
                 start_state: str,
                 final_states: Set[str],
                 transitions: Dict[str, Dict[str, Set[str]]]) -> None:
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.start_state = start_state
        self.final_states = set(final_states)
        # transitions[state][symbol] -> set(next_states)
        self.transitions: Dict[str, Dict[str, Set[str]]] = {}
        for s, sym_map in transitions.items():
            self.transitions.setdefault(s, {})
            for sym, dests in sym_map.items():
                self.transitions[s].setdefault(sym, set()).update(dests)

    # ---------- Construction / IO ----------
    @staticmethod
    def from_json(path: str) -> "FiniteAutomaton":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        states = set(data["states"]) if "states" in data else set()
        alphabet = set(data.get("alphabet", []))
        start_state = data["start_state"]
        final_states = set(data.get("final_states", []))
        transitions_raw = data.get("transitions", [])
        transitions: Dict[str, Dict[str, Set[str]]] = {}
        for t in transitions_raw:
            frm = t["from"]; sym = t["symbol"]; to = t["to"]
            transitions.setdefault(frm, {}).setdefault(sym, set()).add(to)
            states.add(frm); states.add(to)
            if sym != EPSILON:
                alphabet.add(sym)
        fa = FiniteAutomaton(states, alphabet, start_state, final_states, transitions)
        fa.validate()
        return fa

    # ---------- Validation ----------
    def validate(self) -> None:
        if self.start_state not in self.states:
            raise ValueError("start_state not in states")
        if not self.final_states.issubset(self.states):
            raise ValueError("final_states not subset of states")
        for s, mp in self.transitions.items():
            if s not in self.states:
                raise ValueError(f"transition from unknown state {s}")
            for sym, dests in mp.items():
                if sym != EPSILON and sym not in self.alphabet:
                    raise ValueError(f"transition symbol {sym} not in alphabet")
                for d in dests:
                    if d not in self.states:
                        raise ValueError(f"transition to unknown state {d}")

    # ---------- FA operations ----------
    def move(self, state_set: Set[str], symbol: str) -> Set[str]:
        """
        from a set of states, find all next states you can go to on a given symbol.
        """
        result: Set[str] = set()
        for s in state_set:
            if s not in self.transitions or symbol not in self.transitions[s]:
                return set()
            result.update(self.transitions[s][symbol])
        return result

    def accepts(self, input_string: str) -> bool:
        current_states = {self.start_state}
        for c in input_string:
            if c not in self.alphabet:
                return False
            current_states = self.move(current_states, c)
            if not current_states:
                return False
        return len(current_states.intersection(self.final_states)) > 0

    # (DFA determinization/minimization removed - not used by current CLI)

    # ---------- Pretty Print ----------
    def pretty_print(self) -> str:
        lines: List[str] = []
        lines.append("States: " + ", ".join(sorted(self.states)))
        lines.append("Alphabet: " + ", ".join(sorted(self.alphabet)))
        lines.append("Start: " + self.start_state)
        lines.append("Finals: " + ", ".join(sorted(self.final_states)))
        lines.append("Transitions:")
        for s in sorted(self.states):
            for sym, dests in sorted(self.transitions.get(s, {}).items()):
                lines.append(f"  {s} -{sym}-> {','.join(sorted(dests))}")
        return "\n".join(lines)


# ---------- CLI ----------
def _format_rg(rules: List[Tuple[str, List[str]]]) -> str:
    lines: List[str] = []
    for lhs, prods in rules:
        rhs = " | ".join(prods)
        lines.append(f"{lhs} -> {rhs}")
    return "\n".join(lines)

def fa_to_rg(fa: FiniteAutomaton) -> List[Tuple[str, List[str]]]:
    # Create a nonterminal for every state (use the state name itself)
    # For each transition q -a-> p we add the production "q -> a p"
    # For each final state q we add the production "q -> ε"
    # Finally, we return the productions ordered with the start state first
    rules_map: Dict[str, List[str]] = {s: [] for s in sorted(fa.states)}

    # Loop through states in sorted order so output is deterministic
    for s in sorted(fa.states):
        trans = fa.transitions.get(s, {})

        # For each alphabet symbol add productions "s -> a <dest>"
        for a in sorted(fa.alphabet):
            for p in sorted(trans.get(a, set())):
                rules_map[s].append(f"{a}{p}")

        # If the state is final, it can also produce ε
        if s in fa.final_states:
            rules_map[s].append(EPSILON)

    # Ensure the start state is the first rule, then the others alphabetically
    order = [fa.start_state] + [s for s in sorted(fa.states) if s != fa.start_state]
    return [(s, rules_map[s]) for s in order]

def cmd_accept(args: argparse.Namespace) -> int:
    fa = FiniteAutomaton.from_json(args.fa)
    def run_one(s: str) -> str:
        return f"{s}\tACCEPT" if fa.accepts(s) else f"{s}\tREJECT"

    results: List[str] = []
    if args.inputs.startswith("file:"):
        path = args.inputs.split(":", 1)[1]
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.rstrip("\n")
                if s:
                    results.append(run_one(s))
    else:
        results.append(run_one(args.inputs))

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write("\n".join(results) + "\n")
    else:
        print("\n".join(results))
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    fa = FiniteAutomaton.from_json(args.fa)
    print(fa.pretty_print())
    return 0


# (File-based RG→FA command removed; use rgprint with built-ins.)

def cmd_demo(args: argparse.Namespace) -> int:
    # Compact demo: run sample accepts for handwritten FAs only.
    print("=== Identifier FA (handwritten) ===")
    id_fa = FiniteAutomaton.from_json("lab4/fa_identifier.json")
    print("Identifier samples:")
    for s in ["foo", "_x9", "9bad"]:
        verdict = "ACCEPT" if id_fa.accepts(s) else "REJECT"
        print(f"  {s}\t{verdict}")

    print("\n=== Number FA (handwritten) ===")
    num_fa = FiniteAutomaton.from_json("lab4/fa_number.json")
    print("Number samples:")
    for s in ["0", "123", "a1"]:
        verdict = "ACCEPT" if num_fa.accepts(s) else "REJECT"
        print(f"  {s}\t{verdict}")

    # Also show FA -> RG grammars for both
    print("\nGrammar (identifier from FA):")
    print(_format_rg(fa_to_rg(id_fa)))
    print("\nGrammar (number from FA):")
    print(_format_rg(fa_to_rg(num_fa)))

    return 0

def cmd_fa2rg(args: argparse.Namespace) -> int:
    fa = FiniteAutomaton.from_json(args.fa)
    rules = fa_to_rg(fa)
    print(_format_rg(rules))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="FA/RG toolkit for Lab 4")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("accept", help="Validate input(s) against FA JSON")
    a.add_argument("--fa", required=True, help="Path to FA JSON")
    a.add_argument("--input", dest="inputs", required=True, help="String or file:path")
    a.add_argument("--out", help="Optional output file")
    a.set_defaults(func=cmd_accept)

    s = sub.add_parser("show", help="Pretty print FA JSON")
    s.add_argument("--fa", required=True, help="Path to FA JSON")
    s.set_defaults(func=cmd_show)

    d = sub.add_parser("demo", help="Show both FAs, sample acceptance, and RG->NFA overviews")
    d.set_defaults(func=cmd_demo)

    fr = sub.add_parser("fa2rg", help="Convert FA JSON to right-linear grammar and print")
    fr.add_argument("--fa", required=True, help="Path to FA JSON")
    fr.set_defaults(func=cmd_fa2rg)

    return p


def main(argv: List[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv[1:])
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))


