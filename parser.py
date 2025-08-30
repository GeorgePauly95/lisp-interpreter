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


operaters = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truerdiv,
    ">": great_than,
    "<": less_than,
}


def define_special_form(operater, operands, global_env):
    if len(operands) != 2:
        return "define Invalid Input"
    name = operands[0]
    if type(name) is not list:
        body = evaluate(operands[1], global_env)
        if type(body) is not tuple:
            global_env[name] = body
            return f"{name} is saved as {body}"
        local_env = body[0]
        global_env[name] = local_env, body[1]
        return f"{name} is saved as {body[1]}"
    name = operands[0][0]
    variables = operands[0][1:]
    local_env = {variable: None for variable in variables}
    body = operands[1]
    global_env[name] = local_env, body
    return f"{name} is saved as {body}"


def if_special_form(operater, operands, global_env):
    if len(operands) == 2:
        predicate, consequent = operands[0], operands[1]
        if evaluate(predicate, global_env) is True:
            return evaluate(consequent)
        return
    elif len(operands) == 3:
        predicate, consequent, alternate = operands[0], operands[1], operands[2]
        if evaluate(predicate, global_env) is True:
            return evaluate(consequent, global_env)
        return evaluate(alternate, global_env)
    return "Ill formed special form"


def lambda_special_form(operater, operands, global_env, local_env={}):
    if type(operater) is not list:
        variables = operands[0]
        if type(variables) is not list:
            return "lambda Invalid Input 1"
        local_env = {variable: None for variable in variables}
        return local_env, operands[-1]
    variables = operater[1]
    if type(variables) is not list:
        return "lambda Invalid Input 2"
    values = operands
    if len(variables) != len(values):
        return "Wrong number of arguments passed to procedure"
    n = len(variables)
    for i in range(n):
        global_env[variables[i]] = values[i]
    global_env["lambda"] = operater[-1]
    return evaluate(global_env["lambda"])


special_forms = {
    "if": if_special_form,
    "define": define_special_form,
    "lambda": lambda_special_form,
}


def evaluate(AST, global_env={}):
    if base_cases_checker(AST, global_env) is not None:
        return base_cases_checker(AST, global_env)
    operater, operands = AST[0], AST[1:]
    if type(operater) is not list:
        if operater in operaters:
            return operaters[operater](*evaluate_operands(operands, global_env))
        elif operater in special_forms:
            return special_forms[operater](operater, operands, global_env)
        elif operater in global_env:
            # print(
            #     f"The operater is: {operater}\n The global environment is: {global_env}"
            # )
            if type(global_env[operater]) is not tuple:
                return evaluate(operater, global_env)(*operands)
            local_env = global_env[operater][0]
            if len(local_env) != len(operands):
                return "Incorrect number of arguments"
            local_env = {
                variable: evaluate(value, global_env)
                for variable, value in zip(list(local_env.keys()), operands)
            }
            # print(f"The local env: {local_env}")
            operater = global_env[operater][1]
            local_env.update(
                {a: global_env[a] for a in global_env if a not in local_env}
            )
            return evaluate(operater, global_env=local_env)
    print(operater[0])
    # ((lambda (x y) (*  x y) 1)
    if operater[0] in special_forms:
        return special_forms[operater[0]](operater, operands, global_env, local_env={})
    new_operater = evaluate(operater)
    return new_operater(*evaluate_operands(operands, global_env))


def evaluate_operands(operands, global_env):
    result = [
        evaluate(operand, global_env)
        if type(operand) is list
        else global_env[operand]
        if operand in global_env
        else operand
        for operand in operands
    ]
    return result


def lisp_interpreter(input):
    return evaluate(read_from_tokens(tokenize(input)))
