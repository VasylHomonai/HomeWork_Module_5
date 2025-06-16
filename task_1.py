def caching_fibonacci():
    cache = {}

    def fibonacci(n):
        if n <= 0:
            return 0
        if n == 1:
            return 1
        # Якщо значення для n вже збережене в кеші то взяти з нього, не обчислюючи знову
        if n in cache:
            return cache[n]
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]
    return fibonacci


# Отримуємо функцію fibonacci
fib = caching_fibonacci()

# Використовуємо функцію fibonacci для обчислення чисел Фібоначчі з використанням кешу
print(fib(10))      # Виведе 55
print(fib(15))      # Виведе 610
print(fib(5))       # Виведе 5


"""
При написанні коду дотримувався рекомендації псевдо коду.
Але можна простіше написати, відразу задати cache = {0: 0, 1: 1} Це навіть ефективніше.
Тоді можна було б не писати умови if n <= 0 та if n == 1
"""
