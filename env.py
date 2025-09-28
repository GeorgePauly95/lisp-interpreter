from operations import add, sub, mul, truerdiv, less_than, great_than

global_env = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truerdiv,
    ">": great_than,
    "<": less_than,
    ("outer",): None,
}


def get_variable(name, env):
    if env is None:
        return None
    elif name in env:
        return env[name]
    return get_variable(name, env[("outer",)])


def set_variable(name, value, env):
    env[name] = value
    return


def create_env(names, values, outer_env):
    inner_env = {name: value for name, value in zip(names, values)}
    inner_env[("outer",)] = outer_env
    return inner_env


def find_env(name, env):
    if env is None:
        return None
    elif name in env:
        return env
    return find_env(name, env[("outer",)])
