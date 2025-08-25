from parser import lisp_interpreter

tests = [
    "(lambda (x) ((lambda (y) (* y 2)) x) 23)",
    # "(begin (define sum +) (sum 1 2))",
    "(define sum +)",
    "sum",
    # "(sum 1 2)",
    # "(define x 7)",
    # "(* x 2)",
    "(define square (lambda (x) (* x x)))",
    "(square 2)",
    "(if (> 4 3) 9)",
]
for test in tests:
    print(f"Input: {test}")
    try:
        print(f"{lisp_interpreter(test)}")
    except Exception as e:
        print(f"Error: {e}")
