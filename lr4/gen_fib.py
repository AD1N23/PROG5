import functools

def fib_elem_gen():
    """Генератор, возвращающий элементы ряда Фибоначчи"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def my_genn():
    """Сопрограмма, которая генерирует список чисел Фибоначчи"""
    fib_gen = fib_elem_gen()  # Создаем генератор Фибоначчи один раз
    while True:
        number_of_fib_elem = yield  # Принимаем количество элементов
        fib_list = [next(fib_gen) for _ in range(number_of_fib_elem)]  # Генерируем список
        yield fib_list  # Возвращаем список

def fib_coroutine(g):
    """Декоратор для инициализации корутины"""
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        gen.send(None)  # Инициализация корутины
        return gen
    return inner

class FibonacchiLst:
    def __init__(self, lst):
        self.lst = lst
        self.fib_numbers = set()
        if lst:
            max_num = max(lst)
            a, b = 0, 1
            while a <= max_num:
                self.fib_numbers.add(a)
                a, b = b, a + b

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        while self.index < len(self.lst):
            current = self.lst[self.index]
            self.index += 1
            if current in self.fib_numbers:
                return current
        raise StopIteration

# Пример использования
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
fib_lst = FibonacchiLst(lst)
print(list(fib_lst))  # Вывод: [0, 1, 2, 3, 5, 8, 1]

# # Применяем декоратор
# my_genn = fib_coroutine(my_genn)
# gen = my_genn()
# print(max(gen.send(20)))







