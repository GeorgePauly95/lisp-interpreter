def tokenize(command):
    tokens = command.replace("(", " ( ").replace(")", " ) ").split(" ")
    return [token for token in tokens if token != " " and token != ""]


def read_from_tokens(tokens):
    if len(tokens) == 0:
        return "Enter a valid expression"
    AST = []
    if len(tokens) == 1:
        return atomize(tokens[0])
    elif tokens[0] == "(":
        return read_from_tokens(tokens[1:])
    token = tokens.pop(0)
    while token != ")":
        if token == "(":
            AST.append(read_from_tokens(tokens))
        else:
            AST.append(atomize(token))
        token = tokens.pop(0)
    return AST


def atomize(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return symbolize(token)


def symbolize(token):
    if token in operations:
        return token
    return "Invalid Token"


def add(*operands):
    try:
        result = operands[0]
        for operand in operands[1:]:
            result += operand
        return result
    except TypeError:
        return "Invalid Input"


def sub(*operands):
    try:
        if len(operands) == 1:
            return 0 - operands[0]
        result = operands[0]
        for operand in operands[1:]:
            result -= operand
        return result
    except TypeError:
        return "Invalid Input"


def mul(*operands):
    try:
        result = operands[0]
        for operand in operands[1:]:
            result *= operand
        return result
    except TypeError:
        return "Invalid Input"


def truerdiv(*operands):
    try:
        if len(operands) == 1:
            return 1 / operands[0]
        result = operands[0]
        for operand in operands[1:]:
            result /= operand
        return result
    except TypeError:
        return "Invalid Input"


def great_than(*operands):
    if len(operands) <= 1:
        return True
    first_oprd, rem_oprds = operands[0], operands[1:]
    result = True
    for oprd in rem_oprds:
        if first_oprd < oprd:
            return False
    return result


def less_than(*operands):
    if len(operands) <= 1:
        return True
    first_oprd, rem_oprds = operands[0], operands[1:]
    result = True
    for oprd in rem_oprds:
        if first_oprd > oprd:
            return False
    return result


operations = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truerdiv,
    ">": great_than,
    "<": less_than,
    "if": "if",
}


def evaluate(AST):
    if type(AST) is not list:
        if type(AST) is int or type(AST) is float:
            return AST
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
    if AST[0] not in operations:
        return "Invalid Input"
    if "Invalid Token" in AST:
        return "Invalid Input"
    # Special forms
    if AST[0] == "if":
        operands = AST[1:]
        if len(operands) != 3:
            return "Invalid Input"
        predicate, consequent, alternate = operands[0], operands[1], operands[2]
        if evaluate(predicate) is True:
            return evaluate(consequent)
        return evaluate(alternate)
    # General
    operation, operands = operations[AST[0]], AST[1:]
    return operation(
        *[
            evaluate(operand) if type(operand) is list else operand
            for operand in operands
        ]
    )


while True:
    scheme_expr = input(">")
    print(f"{evaluate(read_from_tokens(tokenize(scheme_expr)))}")
