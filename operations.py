def add(*operands):
    try:
        result = operands[0]
        for operand in operands[1:]:
            result += operand
        return result
    except IndexError:
        return 0
    except TypeError:
        return "add Invalid Input"


def sub(*operands):
    try:
        if len(operands) == 1:
            return 0 - operands[0]
        result = operands[0]
        for operand in operands[1:]:
            result -= operand
        return result
    except IndexError:
        return "Wrong number of arguments passed to procedure"
    except TypeError:
        return "sub Invalid Input"


def mul(*operands):
    try:
        result = operands[0]
        for operand in operands[1:]:
            result *= operand
        return result
    except IndexError:
        return 1
    except TypeError:
        return "mul Invalid Input"


def truerdiv(*operands):
    try:
        if len(operands) == 1:
            return 1 / operands[0]
        result = operands[0]
        for operand in operands[1:]:
            result /= operand
        return result
    except IndexError:
        return "Wrong number of arguments passed to procedure"
    except TypeError:
        return "div Invalid Input"
    except ZeroDivisionError:
        return "Cannot divide by zero"


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
