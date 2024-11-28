# Мегатрейдер

# 1. Основной вклад в сложность даёт двойной цикл, поэтому итоговая вычислительная сложность в худшем случае: O(S * Ln); S - максимальный бюджет, Ln - кол-во лотов
# 2. Субъективная оценка сложности: 8/10, 3 часа

from dataclasses import dataclass
from decimal import Decimal

NOMINAL = Decimal(1000)  # номинал одной облигации, уе
COUPON = Decimal(1)  # стоимость одного купона, уе


@dataclass
class LotDTO:
    """
    Информация о лоте:
        day - порядковый N дня
        name - название облигации
        price - цена, процент от номинала
        quantity - кол-во облигаций в лоте
    """
    day: int
    name: str
    price: Decimal
    quantity: int

    def __str__(self):
        return f"{self.day} {self.name} {self.price} {self.quantity}"


def calculate_lot_data(lot: LotDTO, n: int) -> tuple[Decimal, Decimal]:
    """Доходность лота
    :param lot: лот, для которого расчитывается доходность
    :param n: общая длительность периода торгов, дней
    :return: стоимость лота, доход по лоту
    """
    days_to_maturity = 30 + n - lot.day  # дней до погашения лота

    total_cost = Decimal(lot.price / Decimal(100.0) * NOMINAL * lot.quantity)
    total_income = Decimal((NOMINAL + COUPON * days_to_maturity) * lot.quantity) - total_cost

    return total_cost, total_income


def solve(n_days: int, m_lots_per_day: int, s_amount_total: int, lots: list[LotDTO]) -> tuple[Decimal, list[LotDTO]]:
    """
    Поиск решения для списка лотов
    :param n_days: общая длительность периода торгов, дней
    :param m_lots_per_day: число лотов на рынке в день (максимум)
    :param s_amount_total: бюджет
    :param lots: исходный список лотов
    :return: Итоговый максимальный доход, который можно получить при имеющемся бюджете s_amount_total,
            Список лотов, которые нужно купить для достижения этого дохода.
    """

    # доходность по каждому лоту: total_cost, total_income, lot, исключаем заведомо недоступные для покупки
    lots_data = [(*calculate_lot_data(l, n_days), l) for l in lots if
                 calculate_lot_data(l, n_days)[0] <= s_amount_total]

    dp = [Decimal(0)] * (s_amount_total + 1)  # Максимальная прибыль для каждого бюджета
    lot_selection = [None] * (s_amount_total + 1)  # Список лотов для каждого бюджета
    max_used_budget = 0  # Максимальный использованный бюджет

    for cost, income, lot in lots_data:
        max_budget_to_check = min(s_amount_total, max_used_budget + int(cost))  # Сокращаем область проверки
        for j in range(max_budget_to_check, int(cost) - 1, -1):
            if dp[j - int(cost)] + income > dp[j]:
                # покупка текущего лота даёт лучший результат при бюджете j
                dp[j] = dp[j - int(cost)] + income
                if lot_selection[j - int(cost)] is not None:
                    # Добавляем текущий лот к уже выбранным лотам для бюджета j - cost
                    lot_selection[j] = lot_selection[j - int(cost)] + [lot]
                else:
                    # новый список для бюджета j - cost
                    lot_selection[j] = [lot]
                max_used_budget = max(max_used_budget, j)  # Обновляем максимальный использованный бюджет

    # поиск лучшего бюджета
    max_budget = max(range(max_used_budget + 1),
                     key=lambda x: dp[x])  # бюджет x, для которого значение dp[x] максимально
    selected_lots = lot_selection[max_budget] if lot_selection[max_budget] else []

    return dp[max_budget], selected_lots


if __name__ == "__main__":
    n_days, m_lots_per_day, s_amount_total = [int(x) for x in input("Введите условия N M S через пробел: ").split()]

    lots = []
    print(f"Заполнение данных о лотах на ближайшие {n_days} дней...")
    try:
        while True:
            in_line = input("<день> <название_облигации> <цена> <кол-во> >> ").split(maxsplit=4)
            if len(in_line) < 4:
                break
            lots.append(
                LotDTO(
                    day=int(in_line[0]),
                    name=in_line[1],
                    price=Decimal(in_line[2]),
                    quantity=int(in_line[3]),
                )
            )

    except ValueError:
        print("Ошибка в формате входных данных")
        exit(1)

    max_income, selected_lots = solve(n_days, m_lots_per_day, s_amount_total, lots)

    print(">>> Результаты:")

    print(f"{max_income:.2f}")
    print("\n".join([str(l) for l in selected_lots]))
