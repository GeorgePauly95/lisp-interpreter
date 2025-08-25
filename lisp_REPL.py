from parser import lisp_interpreter

while True:
    scheme_expr = input(">")
    print(f"{lisp_interpreter(scheme_expr)}")
