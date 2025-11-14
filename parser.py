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
        _ = tokens.pop(0)
        while tokens[0] != ")":
            if tokens[0] == "(":
                AST.append(read_from_tokens(tokens))
            else:
                AST.append(atomize(tokens[0]))
            _ = tokens.pop(0)
        return AST
    else:
        return None


def analyze(AST):
    operator, *operands = AST
    if operator == "defmacro":
        return "stores params and body in macro dict"


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
def lambda_special_form(operands, outer_env):
    parameters, body = operands[0], operands[1:]

    # take care of the case where there are no parameters
    def lambda_func(*arguments):
        inner_env = create_env(parameters, arguments, outer_env)
        remaining_body, function_body = body[:-1], body[-1]
        for expression in remaining_body:
            evaluate(expression, inner_env)
        return evaluate(function_body, inner_env)

    return lambda_func


# DEFINE
def define_special_form(operands, env):
    var_name, expression = operands[0], operands[1]
    evaluated_expression = evaluate(expression, env)
    set_variable(var_name, evaluated_expression, env)
    return


# IF
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
    evaluated_expression = evaluate(expression, env)
    variable_env = find_env(variable, env)
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


# QUOTE


def quote_special_form_list(expression, env, depth):
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
        else quote_special_form_list(sub_expr, env, depth)
        for sub_expr in expression
    ]


def quote_special_form(operands, env, depth=1):
    if len(operands) != 1:
        return "Ill formed special form"
    expression = operands[0]
    if type(expression) is not list:
        return expression
    else:
        return quote_special_form_list(expression, env, depth)


# EVALUATOR HELPER FUNCTIONS
def get_operater(AST):
    operater = AST[0]
    return operater


def get_operands(AST):
    operands = AST[1:]
    return operands


### MAIN EVALUATER FUNCTION
def evaluate(AST, env):
    if isinstance(AST, str):
        return get_variable(AST, env)
    elif not isinstance(AST, list):
        return AST

    operater, operands = get_operater(AST), get_operands(AST)
    # check for special forms using a function
    if operater == "if":
        return if_special_form(operands, env)

    elif operater == "define":
        return define_special_form(operands, env)

    elif operater == "lambda":
        return lambda_special_form(operands, env)

    elif operater == "set!":
        return set_special_form(operands, env)

    elif operater == "begin":
        return begin_special_form(operands, env)

    elif operater == "quote":
        return quote_special_form(operands, env)

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


def lisp_interpreter(input):
    return evaluate(read_from_tokens(tokenize(input)), global_env)
