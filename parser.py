from env import global_env, create_env, macro_env
from evaluator import evaluate


def tokenize(command):
    tokens = command.replace("(", " ( ").replace(")", " ) ").split(" ")
    return [token for token in tokens if token != " " and token != ""]


def read_from_tokens(tokens):
    if len(tokens) == 0:
        return None
    if len(tokens) == 1:
        return atomize(tokens[0])
    if tokens[0] == "(":
        AST = []
        _ = tokens.pop(0)
        while tokens[0] != ")":
            if tokens[0] == "(":
                AST.append(read_from_tokens(tokens))
            else:
                AST.append(atomize(tokens[0]))
            _ = tokens.pop(0)
        return AST
    else:
        return None


def analyze(AST):
    if type(AST) is not list:
        return AST
    if len(AST) == 0:
        return AST
    operator, *operands = AST
    print(f"AST: {AST}")
    if operator == "defmacro":
        macro_name, params, body = operands
        macro_env[macro_name] = {"params": params, "body": body}
        return None
    if operator in macro_env:
        params = macro_env[operator]["params"]
        body = macro_env[operator]["body"]
        if len(operands) != len(params):
            return f"Improper number of operands for macro: {operator}"
        env = create_env(params, operands, global_env)
        expanded_expr = evaluate(body, env)
        return analyze(expanded_expr)
    return [analyze(sub_expr) for sub_expr in AST]


def atomize(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token
