from operations import add, sub, mul, truerdiv, less_than, great_than

operations = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truerdiv,
    ">": great_than,
    "<": less_than,
}


def base_cases_checker(AST, global_env):
    if AST is None:
        return "BC Invalid Input 1"

    if type(AST) is not list:
        if type(AST) is int or type(AST) is float:
            return AST
        elif AST in global_env:
            return global_env[AST]
        elif AST in operations:
            return operations[AST]
        return "BC Invalid Input 2"

    if len(AST) == 1:
        operation = AST[0]
        if operation == "+":
            return 0
        elif operation == "*":
            return 1
        elif operation == ">" or operation == "<":
            return True
        return "BC Invalid Input 3"
