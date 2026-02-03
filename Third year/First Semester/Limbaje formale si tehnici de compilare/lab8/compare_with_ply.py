"""
Lab 8 - Requirement 3: Compare GenAI translation with PLY parser results.

This script runs the PLY parser (from Lab 6) on a DSL program
and captures the results for comparison with GenAI-generated C code.
"""

import sys
from pathlib import Path
from io import StringIO

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

import importlib

# Import Lab 6 parser using a normal import so that PLY/inspect
# can correctly locate the source file for the module.
#
# We temporarily add REPO_ROOT to sys.path above, so this works even
# when running the script from subdirectories.
lab6_module = importlib.import_module("lab6.parser")


def run_ply_parser(dsl_file: Path) -> dict:
    """
    Run the PLY parser on a DSL file and capture results.
    
    Returns a dictionary with:
    - valid: bool (whether parsing succeeded)
    - lexical_errors: list of strings
    - syntax_error: str or None
    - productions: list of production strings
    - output: str (full output text)
    """
    result = {
        'valid': False,
        'lexical_errors': [],
        'syntax_error': None,
        'productions': [],
        'output': ''
    }
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured = StringIO()
    
    try:
        # Run the parser
        lab6_module.run_parser(str(dsl_file))
        output = captured.getvalue()
        result['output'] = output
        
        # Parse the output to extract information
        if "Lexical analysis failed" in output:
            # Extract lexical errors
            lines = output.split('\n')
            in_errors = False
            for line in lines:
                if "Errors from Lab5 scanner:" in line:
                    in_errors = True
                    continue
                if in_errors and line.strip().startswith('-'):
                    result['lexical_errors'].append(line.strip()[2:])
        elif "Parsing failed:" in output:
            # Extract syntax error
            for line in output.split('\n'):
                if "Parsing failed:" in line:
                    result['syntax_error'] = line.split("Parsing failed:")[-1].strip()
                    break
        elif "Parsing succeeded" in output:
            result['valid'] = True
            # Extract productions
            in_productions = False
            for line in output.split('\n'):
                if "Production sequence:" in line:
                    in_productions = True
                    continue
                if in_productions and line.strip():
                    result['productions'].append(line.strip())
        
    except Exception as e:
        result['syntax_error'] = f"Exception: {e}"
    finally:
        sys.stdout = old_stdout
    
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python lab8/compare_with_ply.py <dsl_file>")
        print("\nExample:")
        print("  python lab8/compare_with_ply.py lab2/program1.txt")
        return 1
    
    dsl_file = Path(sys.argv[1])
    if not dsl_file.exists():
        print(f"Error: File not found: {dsl_file}")
        return 1
    
    print(f"Running PLY parser on: {dsl_file}")
    print("=" * 60)
    
    result = run_ply_parser(dsl_file)
    
    # Print results
    print("\nPLY Parser Results:")
    # Avoid Unicode checkmarks/crosses for Windows console compatibility
    print(f"  Valid: {'YES' if result['valid'] else 'NO'}")
    
    if result['lexical_errors']:
        print(f"\n  Lexical Errors ({len(result['lexical_errors'])}):")
        for err in result['lexical_errors']:
            print(f"    - {err}")
    
    if result['syntax_error']:
        print(f"\n  Syntax Error:")
        print(f"    {result['syntax_error']}")
    
    if result['valid']:
        print(f"\n  Productions ({len(result['productions'])}):")
        for i, prod in enumerate(result['productions'][:10], 1):  # Show first 10
            print(f"    {i}. {prod}")
        if len(result['productions']) > 10:
            print(f"    ... and {len(result['productions']) - 10} more")
    
    print("\n" + "=" * 60)
    print("Full Output:")
    print(result['output'])
    
    return 0 if result['valid'] else 1


if __name__ == "__main__":
    raise SystemExit(main())


