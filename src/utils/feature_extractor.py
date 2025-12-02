import ast
import re

# Funciones del proyecto que se consideran peligrosas
DANGEROUS_FUNCTIONS = [
    "eval", "exec", "subprocess", "Popen",
    "system", "call", "cursor.execute"
]

def get_ast_depth(node, level=0):
    """Calcula recursivamente la profundidad del árbol AST."""
    if not hasattr(node, "body"):
        return level
    try:
        return max(get_ast_depth(n, level + 1) for n in node.body)
    except:
        return level

def extract_features(code: str):
    """Extrae tokens, profundidad del AST y llamadas peligrosas."""
    result = {}

    # Tokens: palabras usadas en el código
    tokens = re.findall(r"[A-Za-z_]+", code)
    result["token_count"] = len(tokens)

    # Árbol AST
    try:
        tree = ast.parse(code)
        result["ast_depth"] = get_ast_depth(tree)
    except:
        result["ast_depth"] = 0

    # Funciones peligrosas
    danger_count = sum(fn in code for fn in DANGEROUS_FUNCTIONS)
    result["danger_calls"] = danger_count

    # Representación como texto para el modelo ML
    text = " ".join(tokens) + f" danger_calls:{danger_count} ast_depth:{result['ast_depth']}"

    return text, result
