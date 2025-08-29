from parser_2 import lisp_interpreter

tests = [
    # lambda test cases:
    "(lambda (x) ((lambda (y) (* y 2)) x) 23)",
    # 'begin' test cases:
    "(begin (define sum +) (sum 1 2))",
    # 'define' test cases:
    # 1
    "(define sum +)",
    "sum",
    "(sum 1 2)",
    # 2
    "(define x 7)",
    "(* x 2)",
    # 3
    "(define x (* 1 (+ 1 1)))",
    "(* x x)",
    # 4
    "(define (square x) (* x x))",
    "(square (* 3 3))",
    # 5
    "(define square (lambda (y) (* y y)))",
    "(square 2)",
    # 'if' test cases:
    # 1
    "(if (> 4 3) 9)",
    # scoping
    # 1
    "(define outer-var 100)",
    "(define (test-scope inner-var) (+ outer-var inner-var))",
    "(test-scope 23)",
    # 2
    "(define shadowed 10)",
    "(define (shadow-test shadowed) shadowed)",
    "(shadow-test 99)",
    "shadowed",
]
for test in tests:
    print(f"Input: {test}")
    try:
        print(f"Output: {lisp_interpreter(test)}\n")
    except Exception as e:
        print(f"Error: {e}\n")
