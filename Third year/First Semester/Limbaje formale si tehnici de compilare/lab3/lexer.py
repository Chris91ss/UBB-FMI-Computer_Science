import re
import sys
from symbol_table import SymbolTable

# Keywords from Lab 1 BNF
KEYWORDS = {
    "quest", "requires", "objectives", "rewards", "on_accept", "on_update", "on_complete",
    "npc", "item", "location", "dialog", "line", "go_to", "talk_to", "collect", 
    "defeat", "interact", "custom", "set", "give", "take", "spawn", "at", "unlock", 
    "print", "if", "while", "for", "in", "end", "when", "enter", "talk", "pickup", 
    "kill", "timer", "quest_state", "xp", "gold", "flag", "count"
}

# Regex for tokenizing
TOKEN_REGEX = re.compile(r'''
    (?P<WHITESPACE> [ \t\r]+ )                 # spaces / tabs / carriage return
  | (?P<NEWLINE>    \n )                       # newline
  | (?P<COMMENT>    \#[^\n]* )                # line comment starting with '#'
  | (?P<STRING>     \"[^\"\n]*\" )        # string in double quotes (no newlines)
  | (?P<NUMBER>     0|[1-9][0-9]* )            # integer number
  | (?P<OP>         ==|!=|<=|>=|\.\.|=|<|> )  # operators
  | (?P<SEP>        [\{\}\(\),:;] )         # separators
  | (?P<IDENT>      [A-Za-z][A-Za-z0-9_]* )    # identifier / keyword / boolean / logical
  | (?P<UNKNOWN>    . )                        # any other single character
''', re.VERBOSE)


class Lexer:
    def __init__(self):
        self.st = SymbolTable()
        # Each PIF row: {"type": str, "lexeme": str, "st_bucket": int|None, "st_position": int|None}
        self.pif = []
        self.errors = []

    def add_to_pif(self, token_type, token, st_bucket=None, st_position=None):
        self.pif.append({"type": token_type, "lexeme": token, "st_bucket": st_bucket, "st_position": st_position})

    def add_to_st_and_pif(self, lexeme):
        bucket, position = self.st.insert(lexeme)
        self.add_to_pif("CONST_OR_IDENT", lexeme, bucket, position)

    def tokenize(self, text):
        line = 1
        pos = 0
        
        while pos < len(text):
            match = TOKEN_REGEX.match(text, pos)
            if not match:
                break
                
            token_type = match.lastgroup
            lexeme = match.group(token_type)
            
            if token_type == "WHITESPACE" or token_type == "COMMENT":
                pass
            elif token_type == "NEWLINE":
                line += 1
            elif token_type == "STRING":
                self.add_to_st_and_pif(lexeme)
            elif token_type == "NUMBER":
                self.add_to_st_and_pif(lexeme)
            elif token_type == "IDENT":
                if lexeme in {"true", "false"}:
                    self.add_to_st_and_pif(lexeme)
                elif lexeme in KEYWORDS or lexeme in {"and", "or", "not"}:
                    t = "KEYWORD" if lexeme in KEYWORDS else "LOGICAL"
                    self.add_to_pif(t, lexeme, None, None)
                else:
                    self.add_to_st_and_pif(lexeme)
            elif token_type in ["OP", "SEP"]:
                self.add_to_pif(token_type, lexeme, None, None)
            elif token_type == "UNKNOWN":
                if lexeme == '"':
                    end = text.find("\n", pos + 1)
                    snippet = text[pos:end if end != -1 else len(text)]
                    self.errors.append(f"Unterminated string at line {line}: {snippet}")
                    pos = end if end != -1 else len(text)
                    continue
                self.errors.append(f"Illegal token '{lexeme}' at line {line}")
            
            pos = match.end()

    def run(self, src_path):
        with open(src_path, "r", encoding="utf-8") as f:
            text = f.read()
        self.tokenize(text)
        return {
            "pif": self.pif,
            "st": self.st.dump(),
            "errors": self.errors,
        }


def write_outputs(outputs, base_out):
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python lab3/lexer.py <source_file> [--out out_base]")
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

    # Print to console
    if outputs["errors"]:
        for e in outputs["errors"]:
            print(e)
    else:
        print("No lexical errors.")
    
    # Pretty PIF table
    print("\nPIF:")
    print(f"{'#':>3}  {'TYPE':<14} {'LEXEME':<40} {'BUCKET':>6} {'POS':>3}")
    print("-" * 75)
    for i, row in enumerate(outputs["pif"], 1):
        bucket = -1 if row["st_bucket"] is None else row["st_bucket"]
        pos = -1 if row["st_position"] is None else row["st_position"]
        print(f"{i:>3}  {row['type']:<14} {row['lexeme']:<40} {bucket:>6} {pos:>3}")

    # Pretty ST table
    print("\nST:")
    print(f"{'BUCKET':>6}  {'POS':>3}  LEXEME")
    print("-" * 40)
    for entry in outputs["st"]:
        print(f"{entry['bucket']:>6}  {entry['position']:>3}  {entry['lexeme']}")

    write_outputs(outputs, out_base)
    return 0

if __name__ == "__main__":
    sys.exit(main())


