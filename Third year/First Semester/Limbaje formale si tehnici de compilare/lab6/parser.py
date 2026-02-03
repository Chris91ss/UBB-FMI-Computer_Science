import sys
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

import importlib.util

spec_lab5 = importlib.util.spec_from_file_location(
    "lab5_scanner", REPO_ROOT / "lab5" / "scanner.py"
)
lab5_module = importlib.util.module_from_spec(spec_lab5)
spec_lab5.loader.exec_module(lab5_module)
Lab5Lexer = lab5_module.Lexer

from ply.lex import LexToken
import ply.yacc as yacc

reserved = {
    "quest": "QUEST",
    "requires": "REQUIRES",
    "objectives": "OBJECTIVES",
    "rewards": "REWARDS",
    "on_accept": "ON_ACCEPT",
    "on_update": "ON_UPDATE",
    "on_complete": "ON_COMPLETE",
    "when": "WHEN",
    "enter": "ENTER",
    "talk": "TALK",
    "pickup": "PICKUP",
    "kill": "KILL",
    "go_to": "GO_TO",
    "talk_to": "TALK_TO",
    "collect": "COLLECT",
    "defeat": "DEFEAT",
    "interact": "INTERACT",
    "custom": "CUSTOM",
    "if": "IF",
    "end": "END",
    "set": "SET",
    "print": "PRINT",
    "give": "GIVE",
    "unlock": "UNLOCK",
    "xp": "XP",
    "gold": "GOLD",
    "item": "ITEM",
    "count": "COUNT",
    "and": "AND",
    "or": "OR",
    "not": "NOT",
    "true": "BOOLEAN",
    "false": "BOOLEAN",
}

tokens = [
    "IDENT",
    "NUMBER",
    "STRING",
    "LBRACE",
    "RBRACE",
    "LPAREN",
    "RPAREN",
    "COLON",
    "COMMA",
    "ASSIGN",
    "EQ",
    "NE",
    "LE",
    "GE",
    "LT",
    "GT",
] + list(set(reserved.values()))

OP_TOKEN_MAP = {
    "==": "EQ",
    "!=": "NE",
    "<=": "LE",
    ">=": "GE",
    "=": "ASSIGN",
    "<": "LT",
    ">": "GT",
}

SEP_TOKEN_MAP = {
    "{": "LBRACE",
    "}": "RBRACE",
    "(": "LPAREN",
    ")": "RPAREN",
    ":": "COLON",
    ",": "COMMA",
}

productions_log: List[str] = []


def _strip_quotes(lexeme: str) -> str:
    return lexeme[1:-1]


def build_tokens_from_pif(pif_rows: List[dict]) -> List[LexToken]:
    tokens_out: List[LexToken] = []
    lexpos = 0
    for row in pif_rows:
        tok = LexToken()
        lexeme = row["lexeme"]
        tok.lineno = row.get("line", 0) or 0
        tok.lexpos = lexpos
        lexpos += 1

        if row["type"] == "KEYWORD":
            tok.type = reserved[lexeme]
            tok.value = (
                True if lexeme == "true" else False
                if tok.type == "BOOLEAN"
                else lexeme
            )
        elif row["type"] == "LOGICAL":
            tok.type = reserved[lexeme]
            tok.value = lexeme
        elif row["type"] == "OP":
            token_name = OP_TOKEN_MAP.get(lexeme)
            if not token_name:
                raise SyntaxError(f"Unsupported operator '{lexeme}'")
            tok.type = token_name
            tok.value = lexeme
        elif row["type"] == "SEP":
            token_name = SEP_TOKEN_MAP.get(lexeme)
            if not token_name:
                raise SyntaxError(f"Unsupported separator '{lexeme}'")
            tok.type = token_name
            tok.value = lexeme
        elif row["type"] == "CONST_OR_IDENT":
            if lexeme.startswith('"') and lexeme.endswith('"'):
                tok.type = "STRING"
                tok.value = _strip_quotes(lexeme)
            elif lexeme.isdigit():
                tok.type = "NUMBER"
                tok.value = int(lexeme)
            elif lexeme in {"true", "false"}:
                tok.type = "BOOLEAN"
                tok.value = lexeme == "true"
            else:
                tok.type = "IDENT"
                tok.value = lexeme
        else:
            raise SyntaxError(f"Unknown token category '{row['type']}'")

        productions_log.append(f"token -> {tok.type}")
        tokens_out.append(tok)
    return tokens_out


class PIFLexerAdapter:
    def __init__(self, tokens: List[LexToken]):
        self.tokens = tokens
        self.index = 0

    def token(self):
        if self.index >= len(self.tokens):
            return None
        tok = self.tokens[self.index]
        self.index += 1
        return tok


def log(rule: str):
    productions_log.append(rule)


def p_program(p):
    "program : quest_block when_list opt_if"
    log("program -> quest_block when_list opt_if")


def p_when_list(p):
    """when_list : when_list when_block
                 | empty"""
    if len(p) == 3:
        log("when_list -> when_list when_block")
    else:
        log("when_list -> empty")


def p_opt_if(p):
    """opt_if : IF expression COLON statements END
              | empty"""
    if len(p) == 6:
        log("opt_if -> IF expression COLON statements END")
    else:
        log("opt_if -> empty")


def p_when_block(p):
    "when_block : WHEN event COLON statements END"
    log("when_block -> WHEN event COLON statements END")


def p_event(p):
    """event : ENTER STRING
             | TALK STRING
             | PICKUP STRING
             | KILL STRING"""
    log("event -> EVENT STRING")


def p_quest_block(p):
    "quest_block : QUEST STRING LBRACE quest_body RBRACE"
    log("quest_block -> QUEST STRING LBRACE quest_body RBRACE")


def p_quest_body(p):
    "quest_body : requires_section objectives_section rewards_section hook_sections"
    log("quest_body -> requires objectives rewards hooks")


def p_requires_section(p):
    "requires_section : REQUIRES expression"
    log("requires_section -> REQUIRES expression")


def p_objectives_section(p):
    "objectives_section : OBJECTIVES COLON objective_list"
    log("objectives_section -> OBJECTIVES COLON objective_list")


def p_objective_list(p):
    """objective_list : objective_list COMMA objective
                      | objective"""
    if len(p) == 4:
        log("objective_list -> objective_list COMMA objective")
    else:
        log("objective_list -> objective")


def p_objective(p):
    """objective : GO_TO STRING
                 | TALK_TO STRING
                 | INTERACT STRING
                 | CUSTOM STRING
                 | COLLECT STRING COUNT NUMBER
                 | DEFEAT STRING COUNT NUMBER"""
    log("objective -> pattern")


def p_rewards_section(p):
    "rewards_section : REWARDS COLON reward_list"
    log("rewards_section -> REWARDS COLON reward_list")


def p_reward_list(p):
    """reward_list : reward_list COMMA reward
                   | reward"""
    if len(p) == 4:
        log("reward_list -> reward_list COMMA reward")
    else:
        log("reward_list -> reward")


def p_reward(p):
    """reward : XP NUMBER
              | GOLD NUMBER
              | ITEM STRING opt_count"""
    log("reward -> pattern")


def p_opt_count(p):
    """opt_count : COUNT NUMBER
                 | empty"""
    if len(p) == 3:
        log("opt_count -> COUNT NUMBER")
    else:
        log("opt_count -> empty")


def p_hook_sections(p):
    """hook_sections : hook_sections hook
                     | hook"""
    if len(p) == 3:
        log("hook_sections -> hook_sections hook")
    else:
        log("hook_sections -> hook")


def p_hook(p):
    """hook : ON_ACCEPT COLON statements END
            | ON_UPDATE COLON statements END
            | ON_COMPLETE COLON statements END"""
    log("hook -> HOOK COLON statements END")


def p_statements(p):
    """statements : statements statement
                  | statement"""
    if len(p) == 3:
        log("statements -> statements statement")
    else:
        log("statements -> statement")


def p_statement_print(p):
    "statement : PRINT STRING"
    log("statement -> PRINT STRING")


def p_statement_set(p):
    "statement : SET IDENT ASSIGN literal"
    log("statement -> SET IDENT ASSIGN literal")


def p_statement_give(p):
    "statement : GIVE XP NUMBER"
    log("statement -> GIVE XP NUMBER")


def p_statement_unlock(p):
    "statement : UNLOCK STRING"
    log("statement -> UNLOCK STRING")


def p_statement_nested_if(p):
    "statement : IF expression COLON statements END"
    log("statement -> IF expression COLON statements END")


def p_literal(p):
    """literal : STRING
               | NUMBER
               | BOOLEAN
               | IDENT"""
    log("literal -> value")


precedence = (
    ("left", "OR"),
    ("left", "AND"),
    ("nonassoc", "EQ", "NE", "LT", "LE", "GT", "GE"),
)


def p_expression_binary(p):
    """expression : expression AND expression
                  | expression OR expression
                  | expression EQ expression
                  | expression NE expression
                  | expression LE expression
                  | expression GE expression
                  | expression LT expression
                  | expression GT expression"""
    log("expression -> expression op expression")


def p_expression_not(p):
    "expression : NOT expression"
    log("expression -> NOT expression")


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    log("expression -> LPAREN expression RPAREN")


def p_expression_atom(p):
    """expression : IDENT
                  | STRING
                  | NUMBER
                  | BOOLEAN"""
    log("expression -> atom")


def p_expression_call(p):
    "expression : IDENT LPAREN argument_list RPAREN"
    log("expression -> IDENT LPAREN argument_list RPAREN")


def p_argument_list(p):
    """argument_list : argument_list COMMA expression
                     | expression"""
    if len(p) == 4:
        log("argument_list -> argument_list COMMA expression")
    else:
        log("argument_list -> expression")


def p_argument_list_empty(p):
    "argument_list : empty"
    log("argument_list -> empty")


def p_empty(p):
    "empty :"
    log("empty -> EPS")


def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at token {p.type} ({p.value})")
    raise SyntaxError("Syntax error at end of input")


parser = yacc.yacc()


def run_parser(source_path: str):
    scanner = Lab5Lexer()
    outputs = scanner.run(source_path)
    if outputs["errors"]:
        print("Lexical analysis failed. Errors from Lab5 scanner:")
        for err in outputs["errors"]:
            print(f"- {err}")
        return

    productions_log.clear()
    token_objects = build_tokens_from_pif(outputs["pif"])
    lexer_adapter = PIFLexerAdapter(token_objects)

    try:
        parser.parse(lexer=lexer_adapter)
        print("Parsing succeeded. Production sequence:")
        for prod in productions_log:
            print(prod)
    except SyntaxError as exc:
        print("Parsing failed:", exc)


def main():
    if len(sys.argv) < 2:
        print("Usage: python lab6/parser.py <source_file>")
        return 2
    run_parser(sys.argv[1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


