#fibonacci

#python
def fib(n):
   if n == 0:
       return 0
   elif n == 1:
       return 1
  else:
       return fib(n - 1) + fib(n - 2)

#scheme
# (def fib (lambda (n) (if (= n 0) 0 (if (= n 1) 1 (+ fib (- n 1)) (+ fib (- n 2)))))))

#countdown

#python
def countdown(n):
   for _ in range(n, 0, -1):
       print(_)

#scheme
# (define countdown (lambda n (if (> n 1) (begin (display n) (countdown (- n 1))))))

#is_prime

#python
def is_prime(n):
    if n == 1:
        return "not prime!"
    elif n == 2:
        return "prime!"
    for factor in range(2, n):
        if n%factor == 0:
            return "Not prime!"
    return "prime!"

#scheme

# (define prime (lambda (n) (begin (define factor  (lambda (k) (if (< k n) (if (= 0 (modulo n k)) 0 (factor (+ k 1))) 1))) (define k 2) (factor k))))      

#factorial

#python
def factorial(n):
    if n == 1:
        return 1
    return n*factorial(n-1)

#scheme
# (define factorial (lambda n (if (= n 1) 1 (* n (factorial (- n 1))))))

