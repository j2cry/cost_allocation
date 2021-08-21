from debts import Debts

records = [
    # еда
    {'payer': 'Катя', 'amount': 7030.93, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя']},
    # мясо
    {'payer': 'Петя', 'amount': 2716.78, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя']},
    # колбаса/сыр
    {'payer': 'Катя', 'amount': 2290, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя']},
    # бензин
    {'payer': 'Петя', 'amount': 788.18, 'sharers': ['Катя', 'Петя']},
    {'payer': 'Петя', 'amount': 1778.15, 'sharers': ['Катя', 'Петя']},
    # транспондер
    {'payer': 'Петя', 'amount': 2225, 'sharers': ['Катя', 'Петя']},
    # еда на заправке
    {'payer': 'Олег', 'amount': 1104, 'sharers': ['Лиза', 'Олег', 'Петя']},
    {'payer': 'Олег', 'amount': 304, 'sharers': ['Катя']},
    # бензин
    {'payer': 'Петя', 'amount': 759.52, 'sharers': ['Катя', 'Петя']},
    # вторая еда на заправке
    {'payer': 'Олег', 'amount': 717, 'sharers': ['Катя', 'Лиза', 'Петя']},
    {'payer': 'Олег', 'amount': 259, 'sharers': ['Олег']},
    # дом
    {'payer': 'Петя', 'amount': 60000, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя']},
    {'payer': 'Петя', 'amount': 10000, 'sharers': ['Катя', 'Петя']},
    # псо
    {'payer': 'Петя', 'amount': 4200, 'sharers': ['Катя', 'Петя']},
    # рускеала
    {'payer': 'Олег', 'amount': 1600, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя']},
    # рускеала еда
    {'payer': 'Олег', 'amount': 714, 'sharers': ['Катя', 'Лиза']},
    {'payer': 'Олег', 'amount': 379, 'sharers': ['Петя']},
    {'payer': 'Олег', 'amount': 533, 'sharers': ['Олег']},
    # бензин
    {'payer': 'Петя', 'amount': 1473, 'sharers': ['Катя', 'Петя']},
    # кивач
    {'payer': 'Олег', 'amount': 800, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя']},
    # бензин
    {'payer': 'Катя', 'amount': 1429.72, 'sharers': ['Катя', 'Петя']},
    # еда на заправке - запись неточна: без детализации!
    {'payer': 'Олег', 'amount': 500, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя']},
    # хоз Пятерочка
    {'payer': 'Олег', 'amount': 964.03, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя']},
    # тут еще можно поделить конфетки и сидр

    # бензин
    {'payer': 'Катя', 'amount': 923.55, 'sharers': ['Катя', 'Петя']},
    # The кухня
    {'payer': 'Олег', 'amount': 710, 'sharers': ['Петя']},
    {'payer': 'Олег', 'amount': 600, 'sharers': ['Катя']},
    {'payer': 'Олег', 'amount': 699, 'sharers': ['Лиза']},
    {'payer': 'Олег', 'amount': 660, 'sharers': ['Олег']},
    # Питкяранта Пятерочка + хлеб
    {'payer': 'Олег', 'amount': 731.09 + 72, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя']},
    # бензин
    {'payer': 'Петя', 'amount': 736.5, 'sharers': ['Катя', 'Петя']},
    # шампуры
    {'payer': 'Олег', 'amount': 300, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя']},
    # кальян
    {'payer': 'Олег', 'amount': 1000, 'sharers': ['Катя', 'Олег', 'Петя']},
    #
    #
    #
    #
    # {'payer': 'Петя', 'amount': 3614, 'sharers': ['Катя', 'Петя']},
]


if __name__ == '__main__':
    travel = Debts()
    travel.clear()
    for rec in records:
        travel.push(rec)

    expenses, debts = travel.calculate()
    print('personal expenses', expenses, '', sep='\n')
    print('mutual debts', debts, sep='\n')
