import settings
import pandas as pd
from pymongo import MongoClient
from collections import namedtuple
from typing import Tuple

RecordInfo = namedtuple('RecordInfo', 'payer amount sharers')


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
        amount = _json.get('amount', None)
        sharers = _json.get('sharers', None)
        if payer and amount and sharers:
            return RecordInfo(payer, amount, sharers)

    def push(self, _json: dict):
        """ Add record to database """
        pass

    def get(self, _id):     # signature can differ
        """ Get record from database """
        pass

    def calculate(self) -> Tuple[pd.Series, pd.DataFrame]:
        """ Calculate mutual debts.
            Returns personal expenses as pandas.Series and mutual debts as pandas.DataFrame
        """
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

        # calc personal expenses including debts
        personal_expenses = pd.Series(dtype='float64')
        for name in mutual_debts.index:
            personal_expenses[name] = mutual_debts.loc[name, :].sum()

        # mutual settlements
        mutual_debts = mutual_debts - mutual_debts.T
        mutual_debts[mutual_debts <= 0] = pd.NA
        mutual_debts.dropna(axis=0, how='all', inplace=True)
        mutual_debts.dropna(axis=1, how='all', inplace=True)
        mutual_debts.fillna(0, inplace=True)

        return personal_expenses, mutual_debts
