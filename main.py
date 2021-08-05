from debts import Debts

if __name__ == '__main__':
    travel = Debts()
    expenses, debts = travel.calculate()
    print('personal expenses', expenses, '', sep='\n')
    print('mutual debts', debts, sep='\n')
