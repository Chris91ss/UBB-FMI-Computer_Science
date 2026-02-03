# Lab 9 - GenAI Code Optimization (LR(0) C Parser)

---

## Overview

In this lab, GenAI is used to **optimize the C implementation of the LR(0) parser** for the mini DSL.
The starting point is the simple C parser from Lab 8 (`lab8/lr0_parser.c`), which:

- reads a sequence of token names from stdin (one per line),
- builds a small demo parse tree with a synthetic root `Program'`,
- prints the **father/sibling table** for the tree.

The goal in Lab 9 is to optimize this C parser for:

1. **Performance** (less overhead, tighter loops),
2. **Memory usage** (remove unused data, reduce global state),
3. **Code quality** (clearer structure, less redundancy),
4. **Compiler-friendliness** (static functions, inlining opportunities).

**Input Code (to optimize):** `lab8/lr0_parser.c`  
**Optimized Code (output):** `lab9/lr0_parser_optimized.c`

---

## Requirement 1: Optimization Prompt and GenAI Response

### Prompt Used

```text
I have a C implementation of a simple LR(0) parser demo.

The code:
- Reads tokens (one per line) from stdin in a "tokens" mode,
- Builds a tiny parse tree with a root "Program'" and a child "Program",
- Adds up to the first N terminal tokens as children under "Program",
- Prints a father/sibling table (id, symbol, parent, sibling).

The file is: lab8/lr0_parser.c

Please optimize this code for:

1. Performance:
   - Remove any unnecessary work done at runtime.
   - Avoid storing or computing data that is never used.
   - Keep the simple behaviour (demo tree) intact.

2. Memory Efficiency:
   - Reduce global mutable state where possible.
   - Use clear compile-time limits instead of oversized arrays.

3. Code Quality:
   - Simplify the structure.
   - Remove unused LR(0) artefacts like ACTION/GOTO tables and ParserState
     if they are not actually used by the demo.
   - Keep naming consistent and descriptive.

4. Compiler-Friendly:
   - Mark small helper functions as static and inline where appropriate.
   - Use fixed-size arrays with clear bounds.

The observable behaviour must stay the same:
- Still read tokens from stdin in "tokens" mode.
- Still build a tiny Program' -> Program -> <first tokens> tree.
- Still print the same father/sibling table format.

Please provide:
1. The optimized C code.
2. A list of optimizations you applied, grouped by category (performance, memory, code quality, compiler-friendly).
3. Any trade-offs or limitations introduced by these optimizations.
```

### GenAI Response Summary

The GenAI response focused on **simplifying and tightening the LR(0) demo parser** rather than changing its behaviour:

- **Performance:**
  - Removed unused LR(0) machinery (ACTION/GOTO tables, `ParserState`).
  - Simplified the parse function to only build the demo tree that is actually used.
  - Reduced stack operations to a single DFS stack for printing the father/sibling table.

- **Memory:**
  - Replaced several loosely-related globals with clearly bounded arrays (`MAX_TOKENS`, `MAX_NODES`, `MAX_CHILDREN`).
  - Removed the unused `grammar` and `num_productions` structures that were never consulted by the demo parse.

- **Code Quality:**
  - Introduced explicit constants for sizes (`MAX_TOKENS`, `MAX_SYMBOL_LEN`, `MAX_CHILDREN`).
  - Grouped related parsing state (`g_tokens`, `g_nodes`, counts) and made helper functions `static` and `inline`.
  - Simplified `main` to a single “tokens” mode with clear error messages.

- **Compiler-Friendly:**
  - Marked small helpers as `static inline` to enable inlining.
  - Reduced global mutable state and function visibility to the translation unit.
  - Used simple loops and fixed-size arrays instead of indirect tables that were never used.

---

## Input Code (Before Optimization) – `lab8/lr0_parser.c` (Excerpt)

```c
// Parse tree node
typedef struct Node {
    int id;
    char symbol[MAX_SYMBOL_LEN];
    int children[20];  // Max 20 children per node
    int num_children;
} Node;

// LR(0) parser state
typedef struct {
    int state_id;
    int num_items;
} ParserState;

// Global grammar (simplified - hardcoded for mini DSL)
Production grammar[MAX_PRODUCTIONS];
int num_productions = 0;
int start_production = 0;

// ACTION and GOTO tables (simplified - would be precomputed)
// In a full implementation, these would be built dynamically
int action_table[MAX_STATES][MAX_TOKENS];
int goto_table[MAX_STATES][MAX_TOKENS];

// Simplified LR(0) parse (demonstration version)
// In a full implementation, this would use proper ACTION/GOTO tables
int parse() {
    // Initialize
    state_stack_top = 0;
    node_stack_top = 0;
    num_nodes = 0;
    token_index = 0;
    
    // Start state
    state_stack[state_stack_top++] = 0;
    
    // Simplified parsing loop
    // This is a demonstration - full version would use proper LR(0) tables
    int root_id = create_node("Program'");
    
    // For demonstration, create a simple parse tree
    // In full implementation, this would follow LR(0) algorithm exactly
    int program_id = create_node("Program");
    add_child(root_id, program_id);
    
    // Create nodes for tokens (simplified)
    for (int i = 0; i < num_tokens && i < 10; i++) {  // Limit for demo
        int token_node_id = create_node(tokens[i].symbol);
        add_child(program_id, token_node_id);
    }
    
    return root_id;
}
```

Even though the file defined grammar, ACTION, and GOTO tables, the **demo parse** never used them. That made the code heavier than necessary for its purpose in Lab 8 and Lab 9.

---

## Output Code (After Optimization) – `lab9/lr0_parser_optimized.c` (Excerpt)

```c
/*
 * Optimized LR(0) Parser in C - based on lab8/lr0_parser.c
 *
 * This version keeps the same observable behaviour:
 *   - Reads token names (one per line) from stdin in "tokens" mode
 *   - Builds a simple parse tree with a synthetic root "Program'"
 *   - Prints a father/sibling table: (id, symbol, parent, sibling)
 */

#define MAX_TOKENS       1000
#define MAX_SYMBOL_LEN   64
#define MAX_CHILDREN     20
#define MAX_NODES        1000

typedef struct {
    char symbol[MAX_SYMBOL_LEN];
} Token;

typedef struct {
    int  id;
    char symbol[MAX_SYMBOL_LEN];
    int  children[MAX_CHILDREN];
    int  num_children;
} Node;

static Token g_tokens[MAX_TOKENS];
static int   g_num_tokens = 0;

static Node  g_nodes[MAX_NODES];
static int   g_num_nodes = 0;

static inline int create_node(const char *symbol) {
    if (g_num_nodes >= MAX_NODES) {
        fprintf(stderr, "Error: node limit exceeded (%d)\n", MAX_NODES);
        exit(1);
    }
    Node *node = &g_nodes[g_num_nodes];
    node->id = g_num_nodes;
    strncpy(node->symbol, symbol, MAX_SYMBOL_LEN - 1);
    node->symbol[MAX_SYMBOL_LEN - 1] = '\0';
    node->num_children = 0;
    return g_num_nodes++;
}

static inline void add_child(int parent_id, int child_id) {
    Node *parent = &g_nodes[parent_id];
    if (parent->num_children < MAX_CHILDREN) {
        parent->children[parent->num_children++] = child_id;
    }
}

static int parse_demo_tree(void) {
    g_num_nodes = 0;

    int root_id    = create_node("Program'");
    int program_id = create_node("Program");
    add_child(root_id, program_id);

    const int max_terminal_children = 10;
    int limit = g_num_tokens < max_terminal_children
                    ? g_num_tokens
                    : max_terminal_children;

    for (int i = 0; i < limit; i++) {
        int leaf_id = create_node(g_tokens[i].symbol);
        add_child(program_id, leaf_id);
    }

    return root_id;
}

static void read_tokens_from_stdin(void) {
    char line[256];
    g_num_tokens = 0;

    while (g_num_tokens < MAX_TOKENS &&
           fgets(line, (int)sizeof line, stdin) != NULL) {
        size_t len = strlen(line);
        if (len && line[len - 1] == '\n') {
            line[--len] = '\0';
        }
        if (!len) {
            continue;
        }
        Token *t = &g_tokens[g_num_tokens];
        strncpy(t->symbol, line, MAX_SYMBOL_LEN - 1);
        t->symbol[MAX_SYMBOL_LEN - 1] = '\0';
        g_num_tokens++;
    }
}
```

The optimized version is **shorter, clearer, and closer to what the demo actually does**.

---

## Requirement 2: Compilation and Execution Results

### Compilation

Compilation command (from `lab9/` directory):

```bash
gcc -std=c99 -Wall -o lr0_parser_optimized.exe lr0_parser_optimized.c
```

**Compilation Status:** ✅ SUCCESS  
**Compiler Output:** *(no warnings or errors)*

### Execution

For a simple test, we fed a short token sequence to the parser:

```bash
echo "QUEST\nSTRING\nLBRACE\nRBRACE" | lr0_parser_optimized.exe tokens
```

**Program Output:**

```text
Father/Sibling table (id, symbol, parent, sibling):
(0, "Program'", -1, -1)
(1, "Program", 0, -1)
(2, "QUEST", 1, 3)
(3, "STRING", 1, 4)
(4, "LBRACE", 1, 5)
(5, "RBRACE", 1, -1)
```

This confirms that:

- The optimized parser still:
  - Treats `Program'` as root,
  - Has `Program` as its only child,
  - Attaches the terminals (QUEST, STRING, LBRACE, RBRACE) as children of `Program`,
  - Prints the correct father/sibling table.

---

## Requirement 3: Optimizations Applied (Categories)

### 1. Performance Optimizations

- **Removed unused LR(0) tables and grammar:**
  - Deleted `action_table`, `goto_table`, `Production grammar[]`, and `ParserState`.
  - The demo parse never consulted these, so they only added memory and compile-time cost.

- **Simplified parse logic:**
  - Replaced a “fake LR(0)” loop with a direct `parse_demo_tree` that:
    - Creates `Program'` and `Program`,
    - Attaches the first N tokens as leaves.
  - This matches the actual behaviour while doing less work.

- **Reduced stack operations:**
  - Kept a single DFS stack for printing, removed unused `state_stack` and `node_stack`.

### 2. Memory Efficiency

- **Explicit, smaller arrays:**
  - Introduced `MAX_TOKENS`, `MAX_NODES`, and `MAX_CHILDREN` constants.
  - Removed large, unused 2D ACTION/GOTO tables.

- **Eliminated unused counters and indexes:**
  - Removed `num_productions`, `start_production`, and `token_index` that were not used by the demo.

### 3. Code Quality Improvements

- **Simplified data model:**
  - Only kept what the demo actually needs: tokens, nodes, and the father/sibling traversal.

- **Clear separation of concerns:**
  - `read_tokens_from_stdin()` – responsible only for input.
  - `parse_demo_tree()` – responsible only for constructing the tree.
  - `print_father_sibling_table()` – responsible only for output formatting.

- **Improved naming and limits:**
  - Constants like `MAX_TOKENS` and `MAX_SYMBOL_LEN` make constraints explicit.
  - Node/child limits are clearly documented.

### 4. Compiler-Friendly Changes

- **Static and inline functions:**
  - Marked helpers as `static inline` to allow inlining and to restrict linkage to this translation unit.

- **Predictable control flow:**
  - Simple `for` loops and explicit bounds help the optimizer.
  - No unused branches or dead code.

---

## Before vs After Comparison (High Level)

| Metric                  | Before (`lab8/lr0_parser.c`) | After (`lab9/lr0_parser_optimized.c`) | Effect                               |
|-------------------------|------------------------------|----------------------------------------|--------------------------------------|
| Lines of code (approx.) | ~200+                        | ~150                                   | Slightly shorter & more focused      |
| Grammar / ACTION / GOTO | Present but unused           | Removed                                | Less memory, simpler binary          |
| Global arrays           | Tokens, nodes, grammar, etc. | Tokens + nodes only                    | Reduced global state                 |
| Stacks                  | State stack + node stack     | DFS stack only                         | Less overhead, simpler logic         |
| Helpers                 | Non-static helpers           | `static inline` helpers                | Better inlining, internal linkage    |
| Behaviour               | Demo Program'/Program tree   | Same                                   | ✅ Functional equivalence maintained |

---

## Conclusion

- The optimization work in Lab 9 **targets the LR(0) C demo parser** from Lab 8.
- The optimized version:
  - Removes unused LR(0) infrastructure,
  - Tightens memory usage,
  - Simplifies the code while keeping the same **father/sibling table output**.
- Compilation and a simple runtime test confirm that the **behaviour is preserved**, while the implementation is more compact, clearer, and easier for the compiler to optimize.

---

## Deliverables

1. **Documentation:** `lab9/DOCUMENTATION.md` (this file)
2. **Optimized Source Code:** `lab9/lr0_parser_optimized.c`
3. **Executable (after compilation):** `lab9/lr0_parser_optimized.exe`

