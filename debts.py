import settings
import pandas as pd
from pymongo import MongoClient
from collections import namedtuple, defaultdict

RecordInfo = namedtuple('RecordInfo', 'payer amount sharers category')


class Debts:
    """ Class for operating with debts database """
    def __init__(self, **kwargs):
        settings.MONGO_COLLECTION = kwargs.get('collection', settings.MONGO_COLLECTION)

        # connect to database
        client = MongoClient(settings.MONGO_SERVER)
        db = client[settings.MONGO_DATABASE]
        self.__collection = db[settings.MONGO_COLLECTION]

    @staticmethod
    def __parse_record(_json: dict):
        """ Parse database record to RecordInfo """
        payer = _json.get('payer', None)
        try:
            amount = float(_json.get('amount', 0))
        except ValueError:
            amount = 0
        sharers = _json.get('sharers', None)
        category = _json.get('category', None)
        if payer and amount and sharers:
            return RecordInfo(payer, amount, sharers, category)

    def push(self, _json: dict, forced=False) -> bool:
        """ Add record to database. Forced adding can duplicate documents in database """
        if not forced and (self.__collection.count_documents(_json) > 0):
            return False
        self.__collection.insert(_json)
        return True

    def clear(self):
        """ Delete all records in database collection """
        self.__collection.delete_many({})

    def get_expenses(self, sharer: str) -> pd.DataFrame:
        """ Get personal expenses aggregated by categories, calculate sum and return as pandas.DataFrame """
        # expenses = pd.DataFrame()
        expenses = defaultdict(float)
        records = self.__collection.find({'sharers': sharer}, {'_id': 0})
        categories = set()
        for record in records:
            record = self.__parse_record(record)
            expenses[record.category if record.category else '---'] += record.amount / len(record.sharers)
            categories.add(record.category)
        expenses = pd.DataFrame(expenses, index=[sharer]).T
        return expenses.append(pd.Series(expenses.sum(axis=0), name='ИТОГО'))

    def get_payments(self, payer: str) -> pd.DataFrame:
        """ Get all payments for `payer` aggregated by categories, calculate sum and return as pandas.DataFrame """
        payments = defaultdict(float)
        records = self.__collection.find({'payer': payer}, {'_id': 0})
        categories = set()
        for record in records:
            record = self.__parse_record(record)
            payments[record.category if record.category else '---'] += record.amount
            categories.add(record.category)
        payments = pd.DataFrame(payments, index=[payer]).T
        return payments.append(pd.Series(payments.sum(axis=0), name='ИТОГО'))

    def get_all(self):
        for rec in self.__collection.find():
            print(rec)

    def get_debts(self) -> pd.DataFrame:
        """ Calculate mutual debts. Returns mutual debts as pandas.DataFrame """
        mutual_debts = pd.DataFrame()
        for record in self.__collection.find():       # iterate through collection
            record = self.__parse_record(record)
            if not record:
                continue        # drop broken records
            # calculate mutual debts
            for sharer in record.sharers:
                try:
                    temp_value = mutual_debts.loc[sharer, record.payer]
                    if pd.isna(temp_value):
                        temp_value = 0
                except KeyError:
                    temp_value = 0
                mutual_debts.loc[sharer, record.payer] = temp_value + record.amount / len(record.sharers)
        mutual_debts.fillna(0, inplace=True)

        # mutual settlements
        for name in mutual_debts.index:
            if name not in mutual_debts.columns:
                mutual_debts[name] = 0
        mutual_debts = mutual_debts - mutual_debts.T
        mutual_debts[mutual_debts <= 0] = pd.NA
        mutual_debts.dropna(axis=0, how='all', inplace=True)
        mutual_debts.dropna(axis=1, how='all', inplace=True)
        mutual_debts.fillna(0, inplace=True)

        # return personal_expenses, mutual_debts
        return mutual_debts
