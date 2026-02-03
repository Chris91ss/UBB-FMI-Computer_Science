"""
Lab 8 - Wrapper script to run C LR(0) parser with Lab 5 scanner integration.

This script:
1. Uses Lab 5 scanner to tokenize DSL source files
2. Converts PIF to token sequence
3. Feeds tokens to the C LR(0) parser
4. Captures and returns the output
"""

import subprocess
import sys
from pathlib import Path
from io import StringIO

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

import importlib.util

# Import Lab 5 scanner
spec_lab5 = importlib.util.spec_from_file_location(
    "lab5_scanner", REPO_ROOT / "lab5" / "scanner.py"
)
lab5_module = importlib.util.module_from_spec(spec_lab5)
spec_lab5.loader.exec_module(lab5_module)
Lab5Lexer = lab5_module.Lexer


def pif_to_tokens(pif_rows):
    """Map Lab5 PIF to terminal names (same as lab7)."""
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


def run_c_lr0_parser(dsl_file: Path, c_parser_exe: Path = None) -> dict:
    """
    Run the C LR(0) parser on a DSL file.
    
    Returns a dictionary with:
    - valid: bool (whether parsing succeeded)
    - output: str (full output text)
    - father_sibling_table: list of tuples (id, symbol, parent, sibling)
    - error: str or None
    """
    if c_parser_exe is None:
        c_parser_exe = Path(__file__).parent / "lr0_parser.exe"
    
    result = {
        'valid': False,
        'output': '',
        'father_sibling_table': [],
        'error': None
    }
    
    # Step 1: Run Lab 5 scanner
    scanner = Lab5Lexer()
    scanner_out = scanner.run(str(dsl_file))
    
    if scanner_out["errors"]:
        result['error'] = f"Lexical errors: {scanner_out['errors']}"
        return result
    
    # Step 2: Convert PIF to tokens
    try:
        tokens = pif_to_tokens(scanner_out["pif"])
    except Exception as e:
        result['error'] = f"Token conversion error: {e}"
        return result
    
    # Step 3: Feed tokens to C parser via stdin
    try:
        token_input = "\n".join(tokens) + "\n"
        
        process = subprocess.run(
            [str(c_parser_exe), "tokens"],
            input=token_input,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        result['output'] = process.stdout + process.stderr
        
        if process.returncode == 0:
            result['valid'] = True
            # Parse father/sibling table from output
            lines = process.stdout.split('\n')
            in_table = False
            for line in lines:
                if "Father/Sibling table" in line:
                    in_table = True
                    continue
                if in_table and line.strip():
                    # Parse line like: (0, "Program'", -1, -1)
                    line = line.strip()
                    if line.startswith('(') and line.endswith(')'):
                        # Extract values
                        content = line[1:-1]  # Remove parentheses
                        parts = [p.strip().strip('"') for p in content.split(',')]
                        if len(parts) == 4:
                            try:
                                node_id = int(parts[0])
                                symbol = parts[1]
                                parent_id = int(parts[2])
                                sibling_id = int(parts[3])
                                result['father_sibling_table'].append((node_id, symbol, parent_id, sibling_id))
                            except ValueError:
                                pass
        else:
            result['error'] = process.stderr or "Parser execution failed"
            
    except FileNotFoundError:
        result['error'] = f"C parser executable not found: {c_parser_exe}"
    except subprocess.TimeoutExpired:
        result['error'] = "Parser execution timed out"
    except Exception as e:
        result['error'] = f"Error running C parser: {e}"
    
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python lab8/run_c_lr0_parser.py <dsl_file> [c_parser_exe]")
        print("\nExample:")
        print("  python lab8/run_c_lr0_parser.py lab2/program1.txt")
        return 1
    
    dsl_file = Path(sys.argv[1])
    if not dsl_file.exists():
        print(f"Error: File not found: {dsl_file}")
        return 1
    
    c_parser_exe = Path(sys.argv[2]) if len(sys.argv) >= 3 else None
    
    print(f"Running C LR(0) parser on: {dsl_file}")
    print("=" * 60)
    
    result = run_c_lr0_parser(dsl_file, c_parser_exe)
    
    # Print results
    print("\nC LR(0) Parser Results:")
    print(f"  Valid: {'YES' if result['valid'] else 'NO'}")
    
    if result['error']:
        print(f"\n  Error: {result['error']}")
    
    if result['valid']:
        print(f"\n  Father/Sibling Table ({len(result['father_sibling_table'])} nodes):")
        for i, row in enumerate(result['father_sibling_table'][:10], 1):
            print(f"    {i}. {row}")
        if len(result['father_sibling_table']) > 10:
            print(f"    ... and {len(result['father_sibling_table']) - 10} more")
    
    print("\n" + "=" * 60)
    print("Full Output:")
    print(result['output'])
    
    return 0 if result['valid'] else 1


if __name__ == "__main__":
    raise SystemExit(main())
