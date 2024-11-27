# Долевое строительство

# 1. Вычислительная сложность: O(n), алгоритм линейно зависит от размера входных данных (n); требуемая память: в т.ч. от размера в памяти хранимых дробей - O(n * log fraction)
# 2. Ограничение на размер входных данных: эмпирическая оценка на macmini m1 16gb 25_000 элементов за 5 сек (10 за 0.0002 сек)
# 3. Субъективная оценка сложности: 2/10, 30 минут на поиск подвоха, изучение Fraction, доп. вопросы

import time

from fractions import Fraction

# ограничение на массив входящих данных (эмпирически)
INPUT_DATA_LIMIT = 100

def calculate_percentages(input_data: list) -> list[Fraction]:
    """
    Доли каждого элемента массива в процентном выражении

    :param input_data: список долей, элементы которого могут быть представлены как рациональное число
    :return: список долей в процентном выражении
    """

    # проверяем входные данные
    try:
        valid_fractions = [Fraction(x) for x in input_data]
    except ValueError as error:
        # логирование ошибок и т.п. рутина
        print(f"Wrong input data value: {str(error)}")
        raise

    fractions_sum = sum(valid_fractions)

    return [f / fractions_sum for f in valid_fractions]


if __name__ == "__main__":
    n_total = int(input(f"Введите количество долей [1..{INPUT_DATA_LIMIT}]:"))
    if (n_total > INPUT_DATA_LIMIT) or (n_total < 1):
        print("Введено некорректное количество долей")
        exit(1)

    input_data = [input("> ") for n in range(n_total)]

    # для эмпирической оценки скорости
    start_time = time.perf_counter()

    result = calculate_percentages(input_data)

    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f"Время выполнения для {n_total}: {total_time:.4f} секунд")

    print(">>> Результаты:")
    # представляем результат построчно с округлением до 3х знаков
    print("\n".join(map(lambda x: f"{x:.3f}", result)))
