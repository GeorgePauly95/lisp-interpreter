def add(*operands):
    try:
        result = operands[0]
        for operand in operands[1:]:
            result += operand
        return result
    except TypeError:
        return "Invalid Input"


def sub(*operands):
    try:
        if len(operands) == 1:
            return 0 - operands[0]
        result = operands[0]
        for operand in operands[1:]:
            result -= operand
        return result
    except TypeError:
        return "Invalid Input"


def mul(*operands):
    try:
        result = operands[0]
        for operand in operands[1:]:
            result *= operand
        return result
    except TypeError:
        return "Invalid Input"


def truerdiv(*operands):
    try:
        if len(operands) == 1:
            return 1 / operands[0]
        result = operands[0]
        for operand in operands[1:]:
            result /= operand
        return result
    except TypeError:
        return "Invalid Input"


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
