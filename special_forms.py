from env import set_variable, create_env, find_env


def lambda_eval(evaluate, operands, outer_env):
    parameters, body = operands[0], operands[1:]

    def lambda_func(*arguments):
        inner_env = create_env(parameters, arguments, outer_env)
        remaining_body, function_body = body[:-1], body[-1]
        for expression in remaining_body:
            evaluate(expression, inner_env)
        return evaluate(function_body, inner_env)

    return lambda_func


def define_eval(evaluate, operands, env):
    var_name, expression = operands[0], operands[1]
    evaluated_expression = evaluate(expression, env)
    set_variable(var_name, evaluated_expression, env)
    return


def if_eval(evaluate, operands, env):
    number_of_operands = len(operands)
    if number_of_operands < 2:
        return "Ill formed special form"
    predicate, consequent = operands[0], operands[1]
    if evaluate(predicate, env) is True:
        return evaluate(consequent, env)
    elif number_of_operands == 3:
        alternate = operands[2]
        return evaluate(alternate, env)
    elif number_of_operands > 3:
        return "Ill formed special form"


def set_eval(evaluate, operands, env):
    variable, expression = operands[0], operands[1]
    evaluated_expression = evaluate(expression, env)
    variable_env = find_env(variable, env)
    if variable_env is None:
        return f"{variable}: Unbound variable"
    set_variable(variable, evaluated_expression, variable_env)
    return


def begin_eval(evaluate, operands, env):
    if operands == []:
        return "Ill formed sepcial form"
    expressions, returned_expression = operands[0:-1], operands[-1]
    for expression in expressions:
        evaluate(expression, env)
    evaluated_expression = evaluate(returned_expression, env)
    return evaluated_expression


def quote_list_eval(evaluate, expression, env, depth):
    def unquote(expression):
        return evaluate(expression, env)

    operator, *operands = expression
    if operator == "unquote" and depth == 1:
        if len(operands) > 1:
            return "Ill formed special form"
        return unquote(operands[0])
    if operator == "unquote" and depth > 1:
        depth -= 1
    if operator == "quote":
        depth += 1
    return [
        sub_expr
        if type(sub_expr) is not list
        else quote_list_eval(evaluate, sub_expr, env, depth)
        for sub_expr in expression
    ]


def quote_eval(evaluate, operands, env, depth=1):
    if len(operands) != 1:
        return "Ill formed special form"
    expression = operands[0]
    if type(expression) is not list:
        return expression
    else:
        return quote_list_eval(evaluate, expression, env, depth)


special_forms = {
    "if": if_eval,
    "define": define_eval,
    "quote": quote_eval,
    "set": set_eval,
    "lambda": lambda_eval,
    "begin": begin_eval,
}


def special_forms_finder(special_form):
    return special_forms[special_form]
