import re
from typing import Iterator, Callable


def generator_numbers(text: str) -> Iterator[float]:
    # знаходимо числа у форматі x.y
    pattern = r'(?<=\s)\d+\.\d+(?=\s)'
    # Знаходемо відразу всі числа в тексті, і почерзі їх віддаємо
    for number in re.findall(pattern, text):
        yield float(number)


def sum_profit(text: str, func: Callable) -> float:
    total_sum = 0
    # Передаємо генератору текст, і під час ітерації по черзі отримуємо з нього всі дійсні числа у форматі float
    for num in func(text):
        total_sum += num
    return round(total_sum, 2)


if __name__ == "__main__":
    text = """Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід,
    доповнений додатковими надходженнями 27.45 і 324.00 доларів."""

    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}$")
