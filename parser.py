from operations import add, sub, mul, truerdiv, less_than, great_than


def tokenize(command):
    tokens = command.replace("(", " ( ").replace(")", " ) ").split(" ")
    return [token for token in tokens if token != " " and token != ""]


def read_from_tokens(tokens):
    if len(tokens) == 0:
        return "Enter a valid expression"
    AST = []
    if len(tokens) == 1:
        return atomize(tokens[0])
    # elif tokens[0] == "(":
    #     return read_from_tokens(tokens[1:])
    token = tokens.pop(0)
    while token != ")":
        if token == "(":
            print(f"output is: {AST}")
            AST.append(read_from_tokens(tokens))
        else:
            AST.append(atomize(token))
        print(f"tokens are: {tokens}")
        token = tokens.pop(0)
    return AST


def atomize(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token


operations = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truerdiv,
    ">": great_than,
    "<": less_than,
    "if": "if",
    "define": "define",
    "lambda": "lambda",
}


def evaluate(AST, vars={}):
    print(f"{AST}")
    if type(AST) is not list:
        if type(AST) is int or type(AST) is float:
            return AST
        if AST in vars:
            return vars[AST]
        if AST in operations:
            return operations[AST]
    if len(AST) == 1:
        if AST[0] == "+":
            return 0
        elif AST[0] == "-":
            return "Invalid Input"
        elif AST[0] == "*":
            return 1
        elif AST[0] == ">" or AST[0] == "<":
            return True
        elif AST[0] == "/":
            return "Invalid Input"
        operands = AST[1:]
        if len(operands) != 3:
            return "Invalid Input"
    # special forms
    # if
    if AST[0] == "if":
        operands = AST[1:]
        if len(operands) != 3:
            return "Invalid Input"
        predicate, consequent, alternate = operands[0], operands[1], operands[2]
        if evaluate(predicate) is True:
            return evaluate(consequent)
        return evaluate(alternate)
    # define
    if AST[0] == "define":
        if len(AST) != 3:
            return "Invalid Input"
        if AST[1] is not list:
            vars[AST[1]] = AST[2]
            return
    if AST[0] not in operations:
        return "Invalid Input"
    # lambda
    if AST[0][0] == "lambda":
        arguments = AST[0][1]
        arguments_values = AST[1:]
        if len(arguments) != len(arguments_values):
            return "Invalid Input"
        n = len(arguments)
        for i in range(n):
            vars[arguments[i]] = arguments_values[i]
        vars["lambda"] = AST[0][-1]
        return evaluate(vars["lambda"])

    # General
    operation, operands = operations[AST[0]], AST[1:]
    return operation(
        *[
            evaluate(operand)
            if type(operand) is list
            else vars[operand]
            if operand in vars
            else operand
            for operand in operands
        ]
    )


while True:
    scheme_expr = input(">")
    print(f"{evaluate(read_from_tokens(tokenize(scheme_expr)))}")
