from operations import add, sub, mul, truerdiv, less_than, great_than


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
        tokens.pop(0)
        while tokens[0] != ")":
            if tokens[0] == "(":
                AST.append(read_from_tokens(tokens))
            else:
                AST.append(atomize(tokens[0]))
            tokens.pop(0)
        return AST
    else:
        return None


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
}


def evaluate(AST, vars={}):
    if AST is None:
        return "Invalid Input"
    if type(AST) is not list:
        if type(AST) is int or type(AST) is float:
            return AST
        elif AST in vars:
            return vars[AST]
        elif AST in operations:
            return operations[AST]
        return "Invalid Input"
    if len(AST) == 1:
        if AST[0] == "+":
            return 0
        elif AST[0] == "*":
            return 1
        elif AST[0] == ">" or AST[0] == "<":
            return True
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
    # variables and values  can be expressions, need not be primitive
    elif AST[0] == "define":
        if len(AST) != 3:
            return "Invalid Input"
        if AST[1] is not list:
            vars[AST[1]] = AST[2]
            return
    # lambda
    # accumulate test cases
    # pytest
    if type(AST[0]) is list:
        # lambda with evaluation
        if AST[0][0] == "lambda":
            arguments = AST[0][1]
            arguments_values = AST[1:]
            if len(arguments) != len(arguments_values):
                return "Wrong number of arguments passed to procedure"
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


def lisp_interpreter(input):
    return evaluate(read_from_tokens(tokenize(input)))
