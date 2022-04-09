import numpy as np

import bson.errors
import pandas as pd
from pymongo import MongoClient
from collections import namedtuple, defaultdict
from bson import ObjectId

RecordInfo = namedtuple('RecordInfo', 'payer amount sharers purpose')


class Debts:
    """ Class for operating with debts database """
    def __init__(self, **kwargs):
        server = kwargs.get('server', None)
        database = kwargs.get('database', None)
        collection = kwargs.get('collection', None)
        # validation
        if not (server and database and collection):
            raise ValueError('`server`, `database` and `collection` are non-zero parameters')
        # connect to database
        client = MongoClient(server)
        db = client[database]
        self.__collection = db[collection]

    @staticmethod
    def __parse_record(_json: dict):
        """ Parse database record to RecordInfo """
        payer = _json.get('payer', None)
        try:
            amount = float(str(_json.get('amount', '')).replace(',', '.'))
        except ValueError:
            amount = 0
        sharers = _json.get('sharers', '').split(' ')
        purpose = _json.get('purpose', None)
        if payer and amount and sharers:
            return RecordInfo(payer, amount, sharers, purpose)

    @staticmethod
    def __convert_id(docs, split=True):
        """ Convert IDs in docs from str to ObjectID """
        # split
        docs_with_id = [d for d in docs if d.get('_id')]
        docs_without_id = [d for d in docs if not d.get('_id')]
        # convert ID or clean from empty str ID
        with_id = list(map(lambda doc: {k: ObjectId(v) if k == '_id' else v for k, v in doc.items()}, docs_with_id))
        without_id = list(map(lambda doc: {k: v for k, v in doc.items() if k != '_id'}, docs_without_id))
        return with_id, without_id if split else with_id

    def get_all(self):
        """ Return list with all records from database and sharers list """
        sharers = self.__collection.find_one({'sharers_list': {'$exists': 1}})
        docs = list(self.__collection.find({'sharers_list': {'$exists': 0}}))
        return docs, sharers['sharers_list'] if sharers else []

    def get_sharers(self):
        sharers = self.__collection.find_one({'sharers_list': {'$exists': 1}})
        return sharers['sharers_list'] if sharers else []

    def update(self, *, docs, sharers):
        """ Add or update records in database """
        _ids = None
        if docs:
            update_docs, push_docs = self.__convert_id(docs)
            for doc in update_docs:
                print(doc)
                self.__collection.update_one({'_id': doc['_id']}, {'$set': doc})
            if push_docs:
                insertion = self.__collection.insert_many(push_docs)
                _ids = [str(_id) for _id in insertion.inserted_ids]
        if sharers:
            self.__collection.update_one({'sharers_list': {'$exists': 1}},
                                         {'$set': {'sharers_list': sharers}}, upsert=True)
        return _ids

    def remove(self, _ids):
        """ Remove records with _id from database """
        try:
            self.__collection.delete_many({'_id': {'$in': [ObjectId(_id) for _id in _ids]}})
        except bson.errors.InvalidId:
            pass

    def clear(self):
        """ Delete all records in database collection """
        self.__collection.delete_many({})

    def get_expenses(self, sharer: str) -> pd.Series:
        """ Get personal expenses aggregated by categories, calculate sum and return as pandas.Series """
        expenses = defaultdict(float)
        records = self.__collection.find({'sharers': {'$regex': sharer}}, {'_id': 0})
        categories = set()
        for record in records:
            record = self.__parse_record(record)
            expenses[record.purpose if record.purpose else '---'] += record.amount / len(record.sharers)
            categories.add(record.purpose)
        expenses = pd.Series(expenses, name='expenses', dtype=np.float)
        summary = pd.Series(expenses.sum(axis=0), index=['Total'], name='expenses')
        return round(pd.concat([expenses, summary]), 2)

    def get_payments(self, payer: str) -> pd.Series:
        """ Get all payments for `payer` aggregated by categories, calculate sum and return as pandas.Series """
        payments = defaultdict(float)
        records = self.__collection.find({'payer': payer}, {'_id': 0})
        categories = set()
        for record in records:
            record = self.__parse_record(record)
            payments[record.purpose if record.purpose else '---'] += record.amount
            categories.add(record.purpose)
        payments = pd.Series(payments, name='payments', dtype=np.float)
        summary = pd.Series(payments.sum(axis=0), index=['Total'], name='payments')
        return round(pd.concat([payments, summary]), 2)

    def get_debts(self, as_dict=True) -> pd.DataFrame:
        """ Calculate mutual debts. Returns mutual debts as pandas.DataFrame """
        mutual_debts = pd.DataFrame()
        for record in self.__collection.find({'sharers_list': {'$exists': 0}}):       # iterate through collection
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

        return round(mutual_debts, 2).to_dict() if as_dict else round(mutual_debts, 2)
