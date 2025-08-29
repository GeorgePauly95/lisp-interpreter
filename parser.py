from operations import add, sub, mul, truerdiv, less_than, great_than
from base_cases import base_cases_checker


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

special_forms = {"if": "if", "define": "define", "lambda": "lambda"}


def evaluate(AST, vars={}):
    if base_cases_checker(AST, vars) is not None:
        return base_cases_checker(AST, vars)
    operation, operands = AST[0], AST[1:]

    if operation == "if":
        # operands = AST[1:]
        if len(operands) == 2:
            predicate, consequent = operands[0], operands[1]
            if evaluate(predicate) is True:
                return evaluate(consequent)
            return
        elif len(operands) == 3:
            predicate, consequent, alternate = operands[0], operands[1], operands[2]
            if evaluate(predicate) is True:
                return evaluate(consequent)
            return evaluate(alternate)
        return "Ill formed special form"

    elif operation == "define":
        if len(AST) != 3:
            return "Invalid Input"
        name = AST[1]
        body = AST[2]
        if type(name) is not list:
            vars[name] = evaluate(body)
            return
        name = AST[1][0]
        arguments = AST[1][1:]
        vars[name] = body
        print(f"{vars}")
        return

    if type(operation) is list:
        if operation[0] == "lambda":
            arguments = operation[1]
            arguments_values = AST[1:]
            if len(arguments) != len(arguments_values):
                return "Wrong number of arguments passed to procedure"
            n = len(arguments)
            for i in range(n):
                vars[arguments[i]] = arguments_values[i]
            vars["lambda"] = operation[-1]
            return evaluate(vars["lambda"])

    if type(operation) is not list:
        if operation in operations:
            return operations[operation](
                *[
                    evaluate(operand)
                    if type(operand) is list
                    else vars[operand]
                    if operand in vars
                    else operand
                    for operand in operands
                ]
            )
        elif operation in vars:
            print(f"{operation}")
            print(f"{vars[operation]}")
            print(f"{evaluate(vars[operation])}")

    return evaluate(operation)(
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
