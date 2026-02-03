"""
Lab 8 - Requirement 3: Compare Lab 6 PLY parser with Lab 7 LR(0) parser (C version).

This script runs both parsers on the same DSL programs and compares their outputs:
- Lab 6 PLY: outputs production sequence
- Lab 7 LR(0) C: outputs father/sibling table

Both represent the same parse tree in different formats.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

# Import comparison functions
from lab8.compare_with_ply import run_ply_parser
from lab8.run_c_lr0_parser import run_c_lr0_parser


def compare_parsers(dsl_file: Path) -> dict:
    """
    Run both parsers and compare results.
    
    Returns a dictionary with comparison results.
    """
    result = {
        'dsl_file': str(dsl_file),
        'ply_result': None,
        'lr0_result': None,
        'both_valid': False,
        'comparison': {}
    }
    
    # Run PLY parser
    print("Running Lab 6 PLY parser...")
    result['ply_result'] = run_ply_parser(dsl_file)
    
    # Run C LR(0) parser
    print("Running Lab 7 LR(0) parser (C)...")
    c_parser_exe = Path(__file__).parent / "lr0_parser.exe"
    result['lr0_result'] = run_c_lr0_parser(dsl_file, c_parser_exe)
    
    # Compare results
    ply_valid = result['ply_result']['valid']
    lr0_valid = result['lr0_result']['valid']
    result['both_valid'] = ply_valid and lr0_valid
    
    result['comparison'] = {
        'both_accept': ply_valid and lr0_valid,
        'both_reject': not ply_valid and not lr0_valid,
        'disagreement': ply_valid != lr0_valid,
        'ply_productions': len(result['ply_result']['productions']) if ply_valid else 0,
        'lr0_nodes': len(result['lr0_result']['father_sibling_table']) if lr0_valid else 0
    }
    
    return result


def print_comparison(result: dict):
    """Print formatted comparison results."""
    print("\n" + "=" * 60)
    print("PARSER COMPARISON RESULTS")
    print("=" * 60)
    
    print(f"\nDSL File: {result['dsl_file']}")
    
    print("\n--- Lab 6 PLY Parser ---")
    ply = result['ply_result']
    print(f"  Status: {'VALID' if ply['valid'] else 'INVALID'}")
    if ply['valid']:
        print(f"  Productions: {len(ply['productions'])}")
        print(f"  First 5 productions:")
        for i, prod in enumerate(ply['productions'][:5], 1):
            print(f"    {i}. {prod}")
    else:
        if ply['syntax_error']:
            print(f"  Error: {ply['syntax_error']}")
        if ply['lexical_errors']:
            print(f"  Lexical Errors: {len(ply['lexical_errors'])}")
    
    print("\n--- Lab 7 LR(0) Parser (C) ---")
    lr0 = result['lr0_result']
    print(f"  Status: {'VALID' if lr0['valid'] else 'INVALID'}")
    if lr0['valid']:
        print(f"  Nodes: {len(lr0['father_sibling_table'])}")
        print(f"  First 5 nodes:")
        for i, node in enumerate(lr0['father_sibling_table'][:5], 1):
            print(f"    {i}. {node}")
    else:
        if lr0['error']:
            print(f"  Error: {lr0['error']}")
    
    print("\n--- Comparison ---")
    comp = result['comparison']
    print(f"  Both parsers accept: {'YES' if comp['both_accept'] else 'NO'}")
    print(f"  Both parsers reject: {'YES' if comp['both_reject'] else 'NO'}")
    print(f"  Disagreement: {'YES' if comp['disagreement'] else 'NO'}")
    
    if comp['both_accept']:
        print(f"\n  PLY Productions: {comp['ply_productions']}")
        print(f"  LR(0) Nodes: {comp['lr0_nodes']}")
        print("\n  Analysis:")
        print("    - Both parsers produce valid parse trees")
        print("    - PLY outputs production sequence (derivation steps)")
        print("    - LR(0) outputs father/sibling table (tree structure)")
        print("    - Both represent the same parse tree in different formats")
        print("    - Production count vs node count may differ:")
        print("      * Productions show internal nodes (reductions)")
        print("      * Nodes include all nodes (internal + terminals)")
    
    if comp['disagreement']:
        print("\n  WARNING: Parsers disagree on validity!")
        print("    This should not happen for equivalent parsers.")
    
    print("\n" + "=" * 60)


def main():
    if len(sys.argv) < 2:
        print("Usage: python lab8/compare_parsers.py <dsl_file>")
        print("\nExample:")
        print("  python lab8/compare_parsers.py lab2/program1.txt")
        return 1
    
    dsl_file = Path(sys.argv[1])
    if not dsl_file.exists():
        print(f"Error: File not found: {dsl_file}")
        return 1
    
    result = compare_parsers(dsl_file)
    print_comparison(result)
    
    return 0 if result['both_valid'] else 1


if __name__ == "__main__":
    raise SystemExit(main())
