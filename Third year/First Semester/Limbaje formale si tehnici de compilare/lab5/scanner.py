import sys
from pathlib import Path
from typing import Dict, Set, List

# Import FiniteAutomaton from Lab 4
import importlib.util
spec = importlib.util.spec_from_file_location("fa_rg_transformation", Path(__file__).parent.parent / "lab4" / "fa_rg_transformation.py")
fa_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fa_module)
FiniteAutomaton = fa_module.FiniteAutomaton

# Import SymbolTable from Lab 3
spec_st = importlib.util.spec_from_file_location("symbol_table", Path(__file__).parent.parent / "lab3" / "symbol_table.py")
st_module = importlib.util.module_from_spec(spec_st)
spec_st.loader.exec_module(st_module)
SymbolTable = st_module.SymbolTable

LAB4_DIR = Path(__file__).resolve().parent.parent / "lab4"


# Keywords from Lab 1 BNF
KEYWORDS = {
    "quest",
    "requires",
    "objectives",
    "rewards",
    "on_accept",
    "on_update",
    "on_complete",
    "npc",
    "item",
    "location",
    "dialog",
    "line",
    "go_to",
    "talk_to",
    "collect",
    "defeat",
    "interact",
    "custom",
    "set",
    "give",
    "take",
    "spawn",
    "at",
    "unlock",
    "print",
    "if",
    "while",
    "for",
    "in",
    "end",
    "when",
    "enter",
    "talk",
    "pickup",
    "kill",
    "timer",
    "quest_state",
    "xp",
    "gold",
    "flag",
    "count",
}

# Operators (multi-char first, then single-char)
OPERATORS = {"==", "!=", "<=", ">=", "..", "=", "<", ">"}
SEPARATORS = {"{", "}", "(", ")", ",", ":", ";"}


class Lexer:
    def __init__(self):
        self.st = SymbolTable()
        self.pif: List[Dict[str, object]] = []
        self.errors: List[str] = []
        self.identifier_fa = FiniteAutomaton.from_json(str(LAB4_DIR / "fa_identifier.json"))
        self.number_fa = FiniteAutomaton.from_json(str(LAB4_DIR / "fa_number.json"))

    def add_to_pif(
        self,
        token_type: str,
        token: str,
        st_bucket=None,
        st_position=None,
        line: int = 0,
    ) -> None:
        self.pif.append(
            {
                "type": token_type,
                "lexeme": token,
                "st_bucket": st_bucket,
                "st_position": st_position,
                "line": line,
            }
        )

    def add_to_st_and_pif(self, lexeme: str, line: int) -> None:
        bucket, position = self.st.insert(lexeme)
        self.add_to_pif("CONST_OR_IDENT", lexeme, bucket, position, line)

    def _is_whitespace(self, c: str) -> bool:
        return c in " \t\r"

    def _is_digit(self, c: str) -> bool:
        return c.isdigit()

    def _is_letter_or_underscore(self, c: str) -> bool:
        return c.isalpha() or c == "_"

    def _is_alnum_or_underscore(self, c: str) -> bool:
        return c.isalnum() or c == "_"

    def tokenize(self, text: str) -> None:
        line = 1
        pos = 0

        while pos < len(text):
            c = text[pos]

            # Skip whitespace
            if self._is_whitespace(c):
                pos += 1
                continue

            # Handle newline
            if c == "\n":
                line += 1
                pos += 1
                continue

            # Handle comments
            if c == "#":
                while pos < len(text) and text[pos] != "\n":
                    pos += 1
                continue

            # Handle strings
            if c == '"':
                start_pos = pos
                pos += 1
                while pos < len(text) and text[pos] != '"':
                    if text[pos] == "\n":
                        snippet = text[start_pos : pos + 1]
                        self.errors.append(f"Unterminated string at line {line}: {snippet}")
                        pos += 1
                        break
                    pos += 1
                else:
                    if pos < len(text):
                        lexeme = text[start_pos : pos + 1]
                        self.add_to_st_and_pif(lexeme, line)
                        pos += 1
                continue

            # Handle multi-char operators (check 2-char first)
            if pos + 1 < len(text):
                two_char = text[pos : pos + 2]
                if two_char in OPERATORS:
                    self.add_to_pif("OP", two_char, None, None, line)
                    pos += 2
                    continue

            # Handle single-char operators
            if c in OPERATORS:
                self.add_to_pif("OP", c, None, None, line)
                pos += 1
                continue

            # Handle separators
            if c in SEPARATORS:
                self.add_to_pif("SEP", c, None, None, line)
                pos += 1
                continue

            # Handle numbers (start with digit)
            if self._is_digit(c):
                start_pos = pos
                while pos < len(text) and self._is_digit(text[pos]):
                    pos += 1
                lexeme = text[start_pos:pos]
                # Validate with FA
                if self.number_fa.accepts(lexeme):
                    self.add_to_st_and_pif(lexeme, line)
                else:
                    self.errors.append(f"Invalid number '{lexeme}' at line {line}")
                continue

            # Handle identifiers (start with letter or underscore)
            if self._is_letter_or_underscore(c):
                start_pos = pos
                while pos < len(text) and self._is_alnum_or_underscore(text[pos]):
                    pos += 1
                lexeme = text[start_pos:pos]
                # Validate with FA
                if not self.identifier_fa.accepts(lexeme):
                    self.errors.append(f"Invalid identifier '{lexeme}' at line {line}")
                elif lexeme in {"true", "false"}:
                    self.add_to_st_and_pif(lexeme, line)
                elif lexeme in KEYWORDS or lexeme in {"and", "or", "not"}:
                    token_kind = "KEYWORD" if lexeme in KEYWORDS else "LOGICAL"
                    self.add_to_pif(token_kind, lexeme, None, None, line)
                else:
                    self.add_to_st_and_pif(lexeme, line)
                continue

            # Unknown character
            self.errors.append(f"Illegal token '{c}' at line {line}")
            pos += 1

    def run(self, src_path: str):
        with open(src_path, "r", encoding="utf-8") as f:
            text = f.read()
        self.tokenize(text)
        return {"pif": self.pif, "st": self.st.dump(), "errors": self.errors}


def write_outputs(outputs, base_out: str) -> None:
    pif = outputs["pif"]
    st = outputs["st"]
    errors = outputs["errors"]

    with open(base_out + "_pif.txt", "w", encoding="utf-8") as f:
        f.write("#\tTYPE\tLEXEME\tBUCKET\tPOS\n")
        for i, row in enumerate(pif, 1):
            bucket = -1 if row["st_bucket"] is None else row["st_bucket"]
            pos = -1 if row["st_position"] is None else row["st_position"]
            f.write(f"{i}\t{row['type']}\t{row['lexeme']}\t{bucket}\t{pos}\n")

    with open(base_out + "_st.txt", "w", encoding="utf-8") as f:
        f.write("BUCKET\tPOS\tLEXEME\n")
        for entry in st:
            f.write(f"{entry['bucket']}\t{entry['position']}\t{entry['lexeme']}\n")

    with open(base_out + "_errors.txt", "w", encoding="utf-8") as f:
        if not errors:
            f.write("No lexical errors.\n")
        else:
            for e in errors:
                f.write(e + "\n")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python lab5/scanner.py <source_file> [--out out_base]")
        return 2

    src = sys.argv[1]
    out_base = src.rsplit(".", 1)[0]

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--out" and i + 1 < len(sys.argv):
            out_base = sys.argv[i + 1]
            i += 2
        else:
            print(f"Unknown arg: {sys.argv[i]}")
            return 2

    lexer = Lexer()
    outputs = lexer.run(src)

    if outputs["errors"]:
        for e in outputs["errors"]:
            print(e)
    else:
        print("No lexical errors.")

    print("\nPIF:")
    print(f"{'#':>3}  {'TYPE':<14} {'LEXEME':<40} {'BUCKET':>6} {'POS':>3}")
    print("-" * 75)
    for i, row in enumerate(outputs["pif"], 1):
        bucket = -1 if row["st_bucket"] is None else row["st_bucket"]
        pos = -1 if row["st_position"] is None else row["st_position"]
        print(f"{i:>3}  {row['type']:<14} {row['lexeme']:<40} {bucket:>6} {pos:>3}")

    print("\nST:")
    print(f"{'BUCKET':>6}  {'POS':>3}  LEXEME")
    print("-" * 40)
    for entry in outputs["st"]:
        print(f"{entry['bucket']:>6}  {entry['position']:>3}  {entry['lexeme']}")

    write_outputs(outputs, out_base)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


