/*
 * Optimized LR(0) Parser in C - based on lab8/lr0_parser.c
 *
 * This version keeps the same observable behaviour:
 *   - Reads token names (one per line) from stdin in "tokens" mode
 *   - Builds a simple parse tree with a synthetic root "Program'"
 *   - Prints a father/sibling table: (id, symbol, parent, sibling)
 *
 * Optimizations vs the original version (lab8/lr0_parser.c):
 *   - Removed unused LR(0) structures (ACTION/GOTO tables, ParserState)
 *   - Reduced global mutable state and introduced clear size constants
 *   - Marked helper functions as static and inlined small ones
 *   - Avoided repeated strlen / buffer scans in the token reader
 *   - Simplified the parse loop (no unused stacks)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

/* -------------------- Tunable limits -------------------- */

#define MAX_TOKENS       1000
#define MAX_SYMBOL_LEN   64
#define MAX_CHILDREN     20
#define MAX_NODES        1000

/* -------------------- Data structures -------------------- */

typedef struct {
    char symbol[MAX_SYMBOL_LEN];
} Token;

typedef struct {
    int  id;
    char symbol[MAX_SYMBOL_LEN];
    int  children[MAX_CHILDREN];
    int  num_children;
} Node;

/* -------------------- Global state -------------------- */

static Token g_tokens[MAX_TOKENS];
static int   g_num_tokens = 0;

static Node  g_nodes[MAX_NODES];
static int   g_num_nodes = 0;

/* -------------------- Helpers -------------------- */

static inline int
create_node(const char *symbol)
{
    if (g_num_nodes >= MAX_NODES) {
        /* Hard fail: in this lab setting, exceeding this is unexpected. */
        fprintf(stderr, "Error: node limit exceeded (%d)\n", MAX_NODES);
        exit(1);
    }

    Node *node = &g_nodes[g_num_nodes];
    node->id = g_num_nodes;
    /* Safe copy with truncation */
    strncpy(node->symbol, symbol, MAX_SYMBOL_LEN - 1);
    node->symbol[MAX_SYMBOL_LEN - 1] = '\0';
    node->num_children = 0;

    return g_num_nodes++;
}

static inline void
add_child(int parent_id, int child_id)
{
    Node *parent = &g_nodes[parent_id];
    if (parent->num_children < MAX_CHILDREN) {
        parent->children[parent->num_children++] = child_id;
    } else {
        /* For lab purposes just warn; real code would handle this better. */
        fprintf(stderr,
                "Warning: MAX_CHILDREN (%d) exceeded for node %d\n",
                MAX_CHILDREN, parent_id);
    }
}

/* -------------------- Father / sibling table -------------------- */

static void
print_father_sibling_table(int root_id)
{
    printf("\nFather/Sibling table (id, symbol, parent, sibling):\n");

    /* Simple manual stack for DFS traversal */
    int stack[MAX_NODES];
    int parent_stack[MAX_NODES];
    int top = 0;

    stack[top]        = root_id;
    parent_stack[top] = -1;
    top++;

    while (top > 0) {
        top--;
        int node_id   = stack[top];
        int parent_id = parent_stack[top];

        Node *node = &g_nodes[node_id];

        int sibling_id = -1;
        if (parent_id >= 0) {
            Node *parent = &g_nodes[parent_id];
            for (int i = 0; i < parent->num_children; i++) {
                if (parent->children[i] == node_id &&
                    i + 1 < parent->num_children) {
                    sibling_id = parent->children[i + 1];
                    break;
                }
            }
        }

        printf("(%d, \"%s\", %d, %d)\n",
               node_id, node->symbol, parent_id, sibling_id);

        /* Push children in reverse order so they are processed left-to-right */
        for (int i = node->num_children - 1; i >= 0; i--) {
            if (top >= MAX_NODES) {
                fprintf(stderr, "Error: DFS stack overflow\n");
                exit(1);
            }
            stack[top]        = node->children[i];
            parent_stack[top] = node_id;
            top++;
        }
    }
}

/* -------------------- Simplified parse -------------------- */

/*
 * This is a *demonstration* parse:
 *   Program' -> Program -> first up to N terminal tokens
 *
 * In a full LR(0) implementation we would drive the construction with
 * ACTION / GOTO tables. For this lab, the important part is that we still
 * output a correct father/sibling style table over the sequence of tokens.
 */
static int
parse_demo_tree(void)
{
    g_num_nodes = 0;

    int root_id    = create_node("Program'");
    int program_id = create_node("Program");
    add_child(root_id, program_id);

    const int max_terminal_children = 10; /* same cap as original version */
    int limit = g_num_tokens < max_terminal_children
                    ? g_num_tokens
                    : max_terminal_children;

    for (int i = 0; i < limit; i++) {
        int leaf_id = create_node(g_tokens[i].symbol);
        add_child(program_id, leaf_id);
    }

    return root_id;
}

/* -------------------- Token reader -------------------- */

static void
read_tokens_from_stdin(void)
{
    char line[256];
    g_num_tokens = 0;

    while (g_num_tokens < MAX_TOKENS &&
           fgets(line, (int)sizeof line, stdin) != NULL) {
        size_t len = strlen(line);
        if (len && line[len - 1] == '\n') {
            line[--len] = '\0';
        }
        if (!len) {
            continue; /* skip empty lines */
        }

        Token *t = &g_tokens[g_num_tokens];
        strncpy(t->symbol, line, MAX_SYMBOL_LEN - 1);
        t->symbol[MAX_SYMBOL_LEN - 1] = '\0';
        g_num_tokens++;
    }

    if (!g_num_tokens) {
        fprintf(stderr, "Error: no tokens read from stdin\n");
    }
}

/* -------------------- main -------------------- */

int
main(int argc, char *argv[])
{
    if (argc < 2) {
        fprintf(stderr,
                "Usage: %s tokens < (tokens from stdin)\n",
                argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "tokens") != 0) {
        fprintf(stderr,
                "Error: only 'tokens' mode is supported in this optimized demo\n");
        fprintf(stderr,
                "       Feed tokens from the Lab 5 scanner via stdin.\n");
        return 1;
    }

    read_tokens_from_stdin();
    if (!g_num_tokens) {
        return 1;
    }

    int root_id = parse_demo_tree();
    print_father_sibling_table(root_id);

    return 0;
}

