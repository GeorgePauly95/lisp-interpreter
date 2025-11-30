from special_forms import special_forms_finder, special_forms
from env import get_variable


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
    if operater in special_forms:
        return special_forms_finder[special_forms](evaluate, operands, env)

    evaluated_operater = evaluate(operater, env)

    if evaluated_operater is not None:
        evaluated_operands = []
        for operand in operands:
            evaluated_operand = evaluate(operand, env)
            if evaluated_operand is None:
                return f"{operand}: Unbound variable"
            evaluated_operands.append(evaluated_operand)
        return evaluated_operater(*evaluated_operands)
    return f"{operater}: Unbound operater"
