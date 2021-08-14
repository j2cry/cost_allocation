from debts import Debts

records = [
    {'payer': 'Kate', 'amount': 7030.93, 'sharers': ['Kate', 'Lisa', 'Oleg', 'Peter']},
    {'payer': 'Peter', 'amount': 2716.78, 'sharers': ['Kate', 'Lisa', 'Oleg', 'Peter']},
    {'payer': 'Kate', 'amount': 2290, 'sharers': ['Kate', 'Lisa', 'Oleg', 'Peter']},

    {'payer': 'Peter', 'amount': 70000, 'sharers': ['Kate', 'Lisa', 'Oleg', 'Peter']},
    {'payer': 'Peter', 'amount': 4200, 'sharers': ['Kate', 'Peter']},
    {'payer': 'Peter', 'amount': 3614, 'sharers': ['Kate', 'Peter']},
]


if __name__ == '__main__':
    travel = Debts()
    # for rec in records:
    #     travel.push(rec)

    expenses, debts = travel.calculate()
    print('personal expenses', expenses, '', sep='\n')
    print('mutual debts', debts, sep='\n')
