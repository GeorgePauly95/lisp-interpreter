from parser import analyze, read_from_tokens, tokenize
from evaluator import evaluate
from env import global_env


def lisp_interpreter(input):
    return evaluate(analyze(read_from_tokens(tokenize(input))), global_env)


while True:
    scheme_expr = input(">")
    print(f"{lisp_interpreter(scheme_expr)}")
