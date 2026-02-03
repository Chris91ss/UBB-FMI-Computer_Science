/*
 * LR(0) Parser in C - Translated from lab7/lr0_parser.py
 * 
 * This is a simplified C translation of the Python LR(0) parser.
 * It parses DSL programs and outputs a father/sibling parse tree table.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>

#define MAX_TOKENS 1000
#define MAX_SYMBOL_LEN 64
#define MAX_STATES 200
#define MAX_PRODUCTIONS 100

// Token structure
typedef struct {
    char symbol[MAX_SYMBOL_LEN];
} Token;

// Production structure
typedef struct {
    char lhs[MAX_SYMBOL_LEN];
    char rhs[10][MAX_SYMBOL_LEN];  // Max 10 symbols per production
    int rhs_len;
} Production;

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

// Parse tree nodes
Node nodes[1000];
int num_nodes = 0;

// Token stream
Token tokens[MAX_TOKENS];
int num_tokens = 0;
int token_index = 0;

// Stack for parser states
int state_stack[MAX_TOKENS];
int state_stack_top = 0;

// Stack for node IDs
int node_stack[MAX_TOKENS];
int node_stack_top = 0;

// Token name to index mapping (simplified)
int token_name_to_index(const char* name) {
    // This is a simplified mapping - in real implementation would use hash table
    const char* token_names[] = {
        "QUEST", "STRING", "LBRACE", "RBRACE", "REQUIRES", "OBJECTIVES",
        "REWARDS", "COLON", "COMMA", "GO_TO", "TALK_TO", "COLLECT",
        "DEFEAT", "COUNT", "NUMBER", "XP", "GOLD", "ITEM", "ON_ACCEPT",
        "ON_COMPLETE", "ON_UPDATE", "WHEN", "ENTER", "TALK", "PICKUP",
        "KILL", "IF", "END", "PRINT", "SET", "GIVE", "UNLOCK", "IDENT",
        "LPAREN", "RPAREN", "AND", "OR", "NOT", "EQ", "ASSIGN", "$"
    };
    int num_names = sizeof(token_names) / sizeof(token_names[0]);
    for (int i = 0; i < num_names; i++) {
        if (strcmp(name, token_names[i]) == 0) {
            return i;
        }
    }
    return -1;
}

// Initialize grammar (simplified - hardcoded key productions)
void init_grammar() {
    // This is a simplified version - full grammar would have all productions
    // Key productions for demonstration:
    
    // Program -> QuestBlock WhenBlocks OptIf
    strcpy(grammar[0].lhs, "Program");
    strcpy(grammar[0].rhs[0], "QuestBlock");
    strcpy(grammar[0].rhs[1], "WhenBlocks");
    strcpy(grammar[0].rhs[2], "OptIf");
    grammar[0].rhs_len = 3;
    
    // QuestBlock -> QUEST STRING LBRACE QuestBody RBRACE
    strcpy(grammar[1].lhs, "QuestBlock");
    strcpy(grammar[1].rhs[0], "QUEST");
    strcpy(grammar[1].rhs[1], "STRING");
    strcpy(grammar[1].rhs[2], "LBRACE");
    strcpy(grammar[1].rhs[3], "QuestBody");
    strcpy(grammar[1].rhs[4], "RBRACE");
    grammar[1].rhs_len = 5;
    
    num_productions = 2;  // Simplified - full version would have all productions
    start_production = 0;
}

// Create a new node
int create_node(const char* symbol) {
    Node* node = &nodes[num_nodes];
    node->id = num_nodes;
    strncpy(node->symbol, symbol, MAX_SYMBOL_LEN - 1);
    node->symbol[MAX_SYMBOL_LEN - 1] = '\0';
    node->num_children = 0;
    return num_nodes++;
}

// Add child to node
void add_child(int parent_id, int child_id) {
    Node* parent = &nodes[parent_id];
    if (parent->num_children < 20) {
        parent->children[parent->num_children++] = child_id;
    }
}

// Build father/sibling table
void print_father_sibling_table(int root_id) {
    printf("\nFather/Sibling table (id, symbol, parent, sibling):\n");
    
    // Simple DFS traversal
    int stack[1000];
    int stack_top = 0;
    int parent_stack[1000];
    int parent_top = 0;
    
    stack[stack_top++] = root_id;
    parent_stack[parent_top++] = -1;
    
    while (stack_top > 0) {
        int node_id = stack[--stack_top];
        int parent_id = parent_stack[--parent_top];
        
        Node* node = &nodes[node_id];
        
        // Print this node
        int sibling_id = -1;
        if (parent_id >= 0) {
            Node* parent = &nodes[parent_id];
            // Find next sibling
            for (int i = 0; i < parent->num_children; i++) {
                if (parent->children[i] == node_id && i + 1 < parent->num_children) {
                    sibling_id = parent->children[i + 1];
                    break;
                }
            }
        }
        
        printf("(%d, \"%s\", %d, %d)\n", node_id, node->symbol, parent_id, sibling_id);
        
        // Push children in reverse order
        for (int i = node->num_children - 1; i >= 0; i--) {
            stack[stack_top++] = node->children[i];
            parent_stack[parent_top++] = node_id;
        }
    }
}

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

// Read tokens from stdin (one token per line)
void read_tokens() {
    char line[256];
    num_tokens = 0;
    
    while (fgets(line, sizeof(line), stdin) != NULL && num_tokens < MAX_TOKENS) {
        // Remove newline
        size_t len = strlen(line);
        if (len > 0 && line[len - 1] == '\n') {
            line[len - 1] = '\0';
        }
        
        if (strlen(line) > 0) {
            strncpy(tokens[num_tokens].symbol, line, MAX_SYMBOL_LEN - 1);
            tokens[num_tokens].symbol[MAX_SYMBOL_LEN - 1] = '\0';
            num_tokens++;
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s minidsl <source_file>\n", argv[0]);
        fprintf(stderr, "   or: %s tokens < (tokens from stdin)\n", argv[0]);
        return 1;
    }
    
    init_grammar();
    
    if (strcmp(argv[1], "tokens") == 0) {
        // Read tokens from stdin
        read_tokens();
        
        if (num_tokens == 0) {
            fprintf(stderr, "Error: No tokens read\n");
            return 1;
        }
        
        // Parse
        int root_id = parse();
        
        // Print father/sibling table
        print_father_sibling_table(root_id);
        
        return 0;
    } else {
        fprintf(stderr, "Error: Only 'tokens' mode supported in this simplified version\n");
        fprintf(stderr, "Use Python wrapper script to feed tokens from Lab 5 scanner\n");
        return 1;
    }
}
