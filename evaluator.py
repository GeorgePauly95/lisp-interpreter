from env import get_variable
from special_forms import (
    if_eval,
    define_eval,
    lambda_eval,
    set_eval,
    begin_eval,
    quote_eval,
)


def get_operater(AST):
    operater = AST[0]
    return operater


def get_operands(AST):
    operands = AST[1:]
    return operands


def evaluate(AST, env):
    if isinstance(AST, str):
        return get_variable(AST, env)
    elif not isinstance(AST, list):
        return AST

    operater, operands = get_operater(AST), get_operands(AST)
    if operater == "if":
        return if_eval(evaluate, operands, env)

    elif operater == "define":
        return define_eval(evaluate, operands, env)

    elif operater == "lambda":
        return lambda_eval(evaluate, operands, env)

    elif operater == "set!":
        return set_eval(evaluate, operands, env)

    elif operater == "begin":
        return begin_eval(evaluate, operands, env)

    elif operater == "quote":
        return quote_eval(evaluate, operands, env)

    evaluated_operater = evaluate(operater, env)

    if evaluated_operater is not None:
        evaluated_operands = []
        for operand in operands:
            evaluated_operand = evaluate(operand, env)
            if evaluated_operand is None:
                return f"{operand}: Unbound variable"
            evaluated_operands.append(evaluated_operand)
        return evaluated_operater(*evaluated_operands)
    return "Error"
