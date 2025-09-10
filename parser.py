from env import global_env, get_variable, set_variable, create_env, find_env


# TOKENIZE
def tokenize(command):
    tokens = command.replace("(", " ( ").replace(")", " ) ").split(" ")
    return [token for token in tokens if token != " " and token != ""]


# READ TOKENS AND FORM ABSTRACT SYNTAX TREE
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


# EVALUATE TOKENS IF INT/FLOAT (SHOULD THIS BE A PART OF EVALUATOR AND NOT RFT?)
def atomize(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token


# SPECIAL FORMS

# LAMBDA
# (lambda (x y) (* x y))
# ((lambda (x y) (* x y)) 3 4)


# This function should do three things:
# 1. returns a function
# 2. points to outer scope
# 3. binds parameters to arguments
def lambda_special_form(operands, outer_env):
    parameters, body = operands[0], operands[1]

    def lambda_func(*arguments):
        inner_env = create_env(parameters, arguments, outer_env)
        return evaluate(body, inner_env)

    return lambda_func


def lambda_special_form_v2(operands, outer_env):
    parameters, body = operands[0], operands[1:]

    # take care of the case where there are no parameters
    def lambda_func(*arguments):
        inner_env = create_env(parameters, arguments, outer_env)
        remaining_body, function_body = body[:-1], body[-1]
        for expression in remaining_body:
            evaluate(expression, outer_env)
        return evaluate(function_body, inner_env)

    return lambda_func


# DEFINE


# (define square (lambda (x) (* x x)))
# (define <variable> <expression>)
def define_special_form(operands, env):
    var_name, expression = operands[0], operands[1]
    evaluated_expression = evaluate(expression, env)
    set_variable(var_name, evaluated_expression, env)
    return


# IF
# (if <predicate> <consequent> <alternate>)
# (if <predicate> <consequent>)
def if_special_form(operands, env):
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


# SET
def set_special_form(operands, env):
    variable, expression = operands[0], operands[1]
    variable_env = find_env(variable, env)
    evaluated_expression = evaluate(expression, variable_env)
    if variable_env is None:
        return f"{variable}: Unbound variable"
    set_variable(variable, evaluated_expression, variable_env)
    return


# BEGIN
def begin_special_form(operands, env):
    if operands == []:
        return "Ill formed sepcial form"
    expressions, returned_expression = operands[0:-1], operands[-1]
    for expression in expressions:
        evaluate(expression, env)
    evaluated_expression = evaluate(returned_expression, env)
    return evaluated_expression


# END OF SPECIAL FORMS


# EVALUATOR HELPER FUNCTIONS
def get_operater(AST):
    operater = AST[0]
    return operater


def get_operands(AST):
    operands = AST[1:]
    return operands


# change AST to expression
def check_base_cases(expression, env):
    if expression is None:
        return "Invalid Input"
    expression_type = type(expression)
    if expression_type is not list:
        if expression_type is int or expression_type is float:
            return expression
        return get_variable(expression, env)
    return None


# ((lambda (x y) (* x y)) 3 4)


### MAIN EVALUATER FUNCTION
def evaluate(AST, env):
    base_case = check_base_cases(AST, env)

    if base_case is not None:
        return base_case

    operater, operands = get_operater(AST), get_operands(AST)
    # check for special forms using a function
    if operater == "if":
        return if_special_form(operands, env)

    elif operater == "define":
        return define_special_form(operands, env)

    elif operater == "lambda":
        return lambda_special_form_v2(operands, env)

    elif operater == "set!":
        return set_special_form(operands, env)

    elif operater == "begin":
        return begin_special_form(operands, env)

    evaluated_operater = evaluate(operater, env)

    if evaluated_operater is not None:
        # need to fix the return value when one of the operands or even the operater are unbound.
        evaluated_operands = [evaluate(operand, env) for operand in operands]
        return evaluated_operater(*evaluated_operands)
    return None


def lisp_interpreter(input):
    return evaluate(read_from_tokens(tokenize(input)), global_env)
