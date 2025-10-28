"""
Анализ анкет из файла
"""
import argparse
import re

def extract_gender_entries(filename, target_gender='Мужской'):
    """
    Находит анкеты по полу и считает их
    """
    male_entries = []  # список мужских анкет
    current_entry = []  # текущая анкета
    is_male = False  # флаг мужской анкеты
    entry_count = 0  # счетчик

    # Читаем файл
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Обрабатываем каждую строку
    for line in lines:
        line = line.strip()

        # Пустая строка - конец анкеты
        if not line:
            if current_entry and is_male:
                male_entries.append('\n'.join(current_entry))
                entry_count += 1
            current_entry = []
            is_male = False
        else:
            current_entry.append(line)
            # Проверяем пол с помощью регулярного выражения
            if re.search(r'^Пол:\s*' + re.escape(target_gender), line):
                is_male = True

    # Последняя анкета
    if current_entry and is_male:
        male_entries.append('\n'.join(current_entry))
        entry_count += 1

    return entry_count, male_entries


def main():
    """
    Главная функция
    """
    try:
        # Создаем парсер аргументов командной строки
        parser = argparse.ArgumentParser(description='Анализ анкет по полу')
        parser.add_argument('filename', help='Имя файла с анкетами')
        args = parser.parse_args()

        input_file = args.filename  # Получаем имя файла из аргументов

        # Ищем мужские анкеты
        count, entries = extract_gender_entries(input_file, 'Мужской')

        # Выводим результат на экран
        print(f"Количество мужских анкет: {count}")

    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()