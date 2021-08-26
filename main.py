from debts import Debts

records = [
    # еда
    {'payer': 'Катя', 'amount': 7030.93, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя'], 'category': 'еда'},
    # мясо
    {'payer': 'Петя', 'amount': 2716.78, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя'], 'category': 'еда'},
    # колбаса/сыр
    {'payer': 'Катя', 'amount': 2290, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя'], 'category': 'еда'},
    # бензин
    {'payer': 'Петя', 'amount': 788.18, 'sharers': ['Катя', 'Петя'], 'category': 'бензин'},
    {'payer': 'Петя', 'amount': 1778.15, 'sharers': ['Катя', 'Петя'], 'category': 'бензин'},
    # транспондер
    {'payer': 'Петя', 'amount': 2225, 'sharers': ['Катя', 'Петя'], 'category': 'проезд'},
    # еда на заправке
    {'payer': 'Олег', 'amount': 1104, 'sharers': ['Лиза', 'Олег', 'Петя'], 'category': 'еда'},
    {'payer': 'Олег', 'amount': 304, 'sharers': ['Катя'], 'category': 'еда'},
    # бензин
    {'payer': 'Петя', 'amount': 759.52, 'sharers': ['Катя', 'Петя'], 'category': 'бензин'},
    # вторая еда на заправке
    {'payer': 'Олег', 'amount': 717, 'sharers': ['Катя', 'Лиза', 'Петя'], 'category': 'еда'},
    {'payer': 'Олег', 'amount': 259, 'sharers': ['Олег'], 'category': 'еда'},
    # дом
    {'payer': 'Петя', 'amount': 60000, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя'], 'category': 'проживание'},
    {'payer': 'Петя', 'amount': 10000, 'sharers': ['Катя', 'Петя'], 'category': 'проживание'},
    # псо
    {'payer': 'Петя', 'amount': 4200, 'sharers': ['Катя', 'Петя'], 'category': 'проживание'},
    # рускеала
    {'payer': 'Олег', 'amount': 1600, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя'], 'category': 'входные билеты'},
    # рускеала еда
    {'payer': 'Олег', 'amount': 714, 'sharers': ['Катя', 'Лиза'], 'category': 'еда'},
    {'payer': 'Олег', 'amount': 379, 'sharers': ['Петя'], 'category': 'еда'},
    {'payer': 'Олег', 'amount': 533, 'sharers': ['Олег'], 'category': 'еда'},
    # бензин
    {'payer': 'Петя', 'amount': 1473, 'sharers': ['Катя', 'Петя'], 'category': 'бензин'},
    # кивач
    {'payer': 'Олег', 'amount': 800, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя'], 'category': 'входные билеты'},
    # бензин
    {'payer': 'Катя', 'amount': 1429.72, 'sharers': ['Катя', 'Петя'], 'category': 'бензин'},
    # еда на заправке - запись неточна: без детализации!
    {'payer': 'Олег', 'amount': 500, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя'], 'category': 'еда'},
    # хоз Пятерочка
    {'payer': 'Олег', 'amount': 964.03, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя'], 'category': 'еда'},
    # тут еще можно поделить конфетки и сидр

    # бензин
    {'payer': 'Катя', 'amount': 923.55, 'sharers': ['Катя', 'Петя'], 'category': 'бензин'},
    # The кухня
    {'payer': 'Олег', 'amount': 710, 'sharers': ['Петя'], 'category': 'еда'},
    {'payer': 'Олег', 'amount': 600, 'sharers': ['Катя'], 'category': 'еда'},
    {'payer': 'Олег', 'amount': 699, 'sharers': ['Лиза'], 'category': 'еда'},
    {'payer': 'Олег', 'amount': 660, 'sharers': ['Олег'], 'category': 'еда'},
    # Питкяранта Пятерочка + хлеб
    {'payer': 'Олег', 'amount': 731.09 + 72, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя'], 'category': 'еда'},
    # бензин
    {'payer': 'Петя', 'amount': 736.5, 'sharers': ['Катя', 'Петя'], 'category': 'бензин'},
    # шампуры
    {'payer': 'Олег', 'amount': 300, 'sharers': ['Катя', 'Лиза', 'Олег', 'Петя'], 'category': 'еда'},
    # кальян
    {'payer': 'Олег', 'amount': 1000, 'sharers': ['Катя', 'Олег', 'Петя'], 'category': 'кальян'},
    # адреналин
    {'payer': 'Петя', 'amount': 180, 'sharers': ['Катя'], 'category': 'еда'},
    # бензин+стики
    {'payer': 'Петя', 'amount': 2116.87, 'sharers': ['Катя', 'Петя'], 'category': 'бензин'},
    {'payer': 'Петя', 'amount': 390, 'sharers': ['Катя', 'Петя'], 'category': 'стики'},
    # бензин
    {'payer': 'Петя', 'amount': 1444.04, 'sharers': ['Катя', 'Петя'], 'category': 'бензин'},
    {'payer': 'Петя', 'amount': 1811.22, 'sharers': ['Катя', 'Петя'], 'category': 'бензин'},
    # транспондер
    {'payer': 'Петя', 'amount': 2225, 'sharers': ['Катя', 'Петя'], 'category': 'проезд'},
]


if __name__ == '__main__':
    travel = Debts()
    # travel.clear()
    # for rec in records:
    #     travel.push(rec, forced=True)

    debts = travel.get_debts()
    # print('personal expenses', expenses, '', sep='\n')
    print('mutual debts', debts, '', sep='\n')

    ex = travel.get_expenses('Катя')
    print('personal expenses', ex, '', sep='\n')

    pay = travel.get_payments('Петя')
    print('personal payments', pay, '', sep='\n')

    # travel.get_all()
