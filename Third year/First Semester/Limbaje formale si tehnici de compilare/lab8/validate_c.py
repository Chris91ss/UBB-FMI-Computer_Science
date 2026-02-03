"""
Lab 8 - Requirement 2: Validate generated C code (LR(0) parser).

This script compiles and runs the C LR(0) parser,
then reports compilation errors, runtime errors, and output.
"""

import subprocess
import sys
from pathlib import Path


def compile_c(c_file: Path) -> tuple[bool, str]:
    """
    Compile a C file using gcc.
    Returns (success, output/error_message).
    """
    exe_file = c_file.with_suffix('.exe')
    try:
        result = subprocess.run(
            ['gcc', '-std=c99', '-Wall', str(c_file), '-o', str(exe_file)],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, f"Compilation successful. Executable: {exe_file}"
        else:
            return False, f"Compilation failed:\n{result.stderr}"
    except FileNotFoundError:
        return False, "Error: gcc not found. Please install gcc compiler."
    except subprocess.TimeoutExpired:
        return False, "Error: Compilation timed out."
    except Exception as e:
        return False, f"Error during compilation: {e}"


def run_c_parser(exe_file: Path, test_tokens: list[str] = None) -> tuple[bool, str, str]:
    """
    Run the C LR(0) parser with test tokens.
    Returns (success, stdout, stderr).
    """
    if test_tokens is None:
        # Default test tokens
        test_tokens = ["QUEST", "STRING", "LBRACE", "RBRACE", "$"]
    
    try:
        token_input = "\n".join(test_tokens) + "\n"
        result = subprocess.run(
            [str(exe_file), "tokens"],
            input=token_input,
            capture_output=True,
            text=True,
            timeout=5
        )
        return True, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Error: Program execution timed out."
    except Exception as e:
        return False, "", f"Error during execution: {e}"


def validate_c_parser(c_file: Path, test_tokens: list[str] = None) -> dict:
    """
    Validate the C LR(0) parser: compile it, run it, and check output.
    
    Returns a dictionary with:
    - compiles: bool
    - compile_message: str
    - runs: bool
    - stdout: str
    - stderr: str
    - has_output: bool
    """
    result = {
        'compiles': False,
        'compile_message': '',
        'runs': False,
        'stdout': '',
        'stderr': '',
        'has_output': False
    }
    
    # Step 1: Compile
    compiles, compile_msg = compile_c(c_file)
    result['compiles'] = compiles
    result['compile_message'] = compile_msg
    
    if not compiles:
        return result
    
    # Step 2: Run
    exe_file = c_file.with_suffix('.exe')
    if exe_file.exists():
        runs, stdout, stderr = run_c_parser(exe_file, test_tokens)
        result['runs'] = runs
        result['stdout'] = stdout
        result['stderr'] = stderr
        result['has_output'] = bool(stdout.strip())
    
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python lab8/validate_c.py <c_file> [test_token1 test_token2 ...]")
        print("\nExample:")
        print("  python lab8/validate_c.py lab8/lr0_parser.c")
        print("  python lab8/validate_c.py lab8/lr0_parser.c QUEST STRING LBRACE")
        return 1
    
    c_file = Path(sys.argv[1])
    if not c_file.exists():
        print(f"Error: File not found: {c_file}")
        return 1
    
    test_tokens = sys.argv[2:] if len(sys.argv) > 2 else None
    
    print(f"Validating C LR(0) parser: {c_file}")
    print("=" * 60)
    
    result = validate_c_parser(c_file, test_tokens)
    
    # Print results
    print(f"\n1. Compilation:")
    print(f"   Status: {'SUCCESS' if result['compiles'] else 'FAILED'}")
    print(f"   Message: {result['compile_message']}")
    
    if result['compiles']:
        print(f"\n2. Execution:")
        print(f"   Status: {'SUCCESS' if result['runs'] else 'FAILED'}")
        if result['stdout']:
            print(f"   Output:\n{result['stdout']}")
        if result['stderr']:
            print(f"   Errors:\n{result['stderr']}")
        
        if result['has_output']:
            print(f"\n3. Output Check:")
            print(f"   Status: SUCCESS (parser produced output)")
        else:
            print(f"\n3. Output Check:")
            print(f"   Status: WARNING (no output produced)")
    
    return 0 if result['compiles'] and result['runs'] else 1


if __name__ == "__main__":
    raise SystemExit(main())
