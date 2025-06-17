import sys
import re
from pathlib import Path


def exit_with_error(message: str):
    print(message)
    sys.exit(1)


# функцію для виконання парсингу рядка логу
def parse_log_line(line: str) -> dict:
    # Перевірка на правильність формату рядка
    pattern = r"^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.+)$"
    match = re.match(pattern, line.strip())
    if not match:
        return {}  # Неправильний формат

    # Ділення рядка логу на 4 частини
    return {
        'date': match.group(1),
        'time': match.group(2),
        'level': match.group(3),
        'message': match.group(4)
    }


# Завантаження лог-файлів
def load_logs(file_path: str) -> list:
    logs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parsed = parse_log_line(line)
                if parsed:  # додається лише якщо словник не пустий
                    logs.append(parsed)
    except FileNotFoundError:
        exit_with_error(f"Файл не знайдено: {file_path}")
    except PermissionError:
        exit_with_error(f"Немає доступу до файлу: {file_path}")
    except UnicodeDecodeError:
        exit_with_error(f"Помилка кодування при читанні файлу: {file_path}")
    except Exception as e:
        exit_with_error(f"Невідома помилка при читанні файлу: {e}")
    return logs


# Фільтрація за рівнем логування
def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(lambda log: log.get('level') == level, logs))


# Підрахунок записів за рівнем логування
def count_logs_by_level(logs: list) -> dict:
    counts = {}
    for log in logs:
        level = log.get("level")
        if level in counts:
            counts[level] += 1
        else:
            counts[level] = 1
    return counts


# Виведення результатів у заданому форматі
def display_log_counts(counts: dict):
    print(f"{'Рівень логування':<16} | {'Кількість':<5}")
    print('-' * 28)
    for level, count in counts.items():
        if level == "ERROR":
            print(f"\033[35m{level:<16}\033[0m | {count:<5}")
        else:
            print(f"{level:<16} | {count:<5}")


if __name__ == "__main__":
    # Провірка на параметри в скрипті
    if len(sys.argv) < 2:
        exit_with_error("Будь ласка, вкажіть шлях до лог файлу (Обов'язковий параметр).")

    param = sys.argv[1]
    path = Path(param)

    logs = load_logs(str(path))
    if not logs:
        exit_with_error("У лог-файлі немає жодного рядка який би відповідав формату!")

    counts = count_logs_by_level(logs)

    # Оброблюємо другий параметр, який є необов'язковим
    if len(sys.argv) >= 3:
        level = sys.argv[2].upper()
        logs_level = filter_logs_by_level(logs=logs, level=level)
        if logs_level:
            display_log_counts(counts)
            print(f"\nДеталі логів для рівня '{level}':")
            for log in logs_level:
                print(f"{log['date']} {log['time']} - {log['message']}")
        else:
            print(f"Рівень логування '{sys.argv[2]}' не знайдено у логах!\n")
            display_log_counts(counts)
    else:
        display_log_counts(counts)


"""
Правильний запуск скрипта з 1 параметром, з командного рядка на Windows: python .\task_3.py files/log.txt
Результат: https://prnt.sc/0dkukNKRJozX

Правильний запуск скрипта з 2 параметрами, з командного рядка на Windows: python .\task_3.py files/log.txt info
Результат: https://prnt.sc/ia1J-g5Ae9VL

Запуск скрипта з командного рядка на Windows, файл не відповідного формату: python .\task_3.py files/log_no_format.txt
Результат: https://prnt.sc/IZZvXShFD9-W

Запуск скрипта без параметрів з командного рядка на Windows: python .\task_3.py
Результат: https://prnt.sc/0SLg4dLfGfDm
"""
