def tokenize(command):
    tokens = command.replace("(", " ( ").replace(")", " ) ").split(" ")
    return [token for token in tokens if token != " " and token != ""]


def read_from_tokens(tokens):
    if len(tokens) == 0:
        return "Enter a valid expression"
    AST = []
    if len(tokens) == 1:
        return atom(tokens[0])
    elif tokens[0] == "(":
        return read_from_tokens(tokens[1:])
    token = tokens.pop(0)
    while token != ")":
        if token == "(":
            AST.append(read_from_tokens(tokens))
        else:
            AST.append(atom(token))
        token = tokens.pop(0)
    return AST


def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return str(token)
