def tokenizer(command):
    return command.replace("(", " ( ").replace(")", " ) ").split()

def read_from_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError("Enter a valid expression")
    token = tokens.pop(0)
    if token == "(":
        L = []
        while tokens[0] != ")":
            L.append(read_from_tokens(tokens))
        tokens.pop(0)
        return L
    elif token == ")":
        raise SyntaxError("No opening parens to close")
    else:
        return token


    

    
