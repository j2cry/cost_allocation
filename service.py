from flask import Flask, render_template, request, redirect
from waitress import serve
from debts import Debts
import settings

app = Flask(__name__)


@app.route(f'{settings.SERVICE_PATH}', methods=['GET', 'POST'])
def debts_index():
    if collection := request.form.get('collection', ''):
        return redirect(f'{settings.SERVICE_PATH}/{collection}')
    params = {'home': settings.SERVICE_PATH,
              'collection': collection if collection else settings.MONGO_COLLECTION}
    return render_template('base.html', page='index.html', **params)


@app.route(f'{settings.SERVICE_PATH}/<collection>', methods=['POST', 'GET'])
def debts_service(collection):
    """ Show HTML interface
        :param collection: mongo database collection name """
    debts = Debts(collection=collection)
    settings.MONGO_COLLECTION = collection
    params = {'home': settings.SERVICE_PATH,
              'collection': collection,
              'forced': settings.ALLOW_DUPLICATES,
              'records': enumerate(debts.get_all(), 1)}
    return render_template('base.html', page='data.html', **params)


@app.route(f'{settings.SERVICE_PATH}/<collection>/add', methods=['POST'])
def debts_add_item(collection):
    """ Add record to database and redirect to main interface
        :param collection: mongo database collection name """
    debts = Debts(collection=collection)
    record = dict(request.form)
    settings.ALLOW_DUPLICATES = bool(record.pop('forced', 0))
    record['sharers'] = record.get('sharers').split()
    debts.push(record, forced=settings.ALLOW_DUPLICATES)
    return redirect(f'{settings.SERVICE_PATH}/{collection}')


@app.route(f'{settings.SERVICE_PATH}/<collection>/remove')
def debts_remove_item(collection):
    """ Remove record from database and redirect to main interface
        :param collection: mongo database collection name """
    debts = Debts(collection=collection)
    if _id := request.args.get('_id', None):
        debts.remove(_id)
    return redirect(f'{settings.SERVICE_PATH}/{collection}')


@app.route(f'{settings.SERVICE_PATH}/<collection>/result', methods=['GET', 'POST'])
def debts_result(collection):
    """ Show result
        :param collection: mongo database collection name """
    debts = Debts(collection=collection)
    payments, expenses = None, None
    if person := request.args.get('person', ''):
        payments = debts.get_payments(person)
        expenses = debts.get_expenses(person)
    params = {'home': settings.SERVICE_PATH,
              'collection': collection,
              '_debts': debts.get_debts(),
              'person': person,
              'payments': payments,
              'expenses': expenses}
    return render_template('base.html', page='result.html', **params)


@app.route(f'{settings.SERVICE_PATH}/about')
def debts_about():
    params = {'home': settings.SERVICE_PATH,
              'collection': settings.MONGO_COLLECTION}
    return render_template('base.html', page='credits.html', **params)


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=settings.APP_PORT)
