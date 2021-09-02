from flask import Flask, render_template, request, redirect
from waitress import serve
from debts import Debts
from settings import SERVICE_PATH

app = Flask(__name__)


@app.route(f'{SERVICE_PATH}', methods=['GET', 'POST'])
def debts_index():
    if collection := request.form.get('collection', ''):
        return redirect(f'{SERVICE_PATH}/{collection}')
    return render_template('index.html')


@app.route(f'{SERVICE_PATH}/<collection>', methods=['POST', 'GET'])
def debts_service(collection):
    """ Show HTML interface
        :param collection: mongo database collection name """
    debts = Debts(collection=collection)
    return render_template('data.html', path=f'{SERVICE_PATH}/{collection}', records=debts.get_all())


@app.route(f'{SERVICE_PATH}/<collection>/add', methods=['POST'])
def debts_add_item(collection):
    """ Add record to database and redirect to main interface
        :param collection: mongo database collection name """
    debts = Debts(collection=collection)
    record = dict(request.form)
    record['sharers'] = record.get('sharers').split()
    debts.push(record)
    return redirect(f'{SERVICE_PATH}/{collection}')


@app.route(f'{SERVICE_PATH}/<collection>/remove')
def debts_remove_item(collection):
    """ Remove record from database and redirect to main interface
        :param collection: mongo database collection name """
    debts = Debts(collection=collection)
    if _id := request.args.get('_id', None):
        debts.remove(_id)
    return redirect(f'{SERVICE_PATH}/{collection}')


@app.route(f'{SERVICE_PATH}/<collection>/result', methods=['GET', 'POST'])
def debts_result(collection):
    """ Show result
        :param collection: mongo database collection name """
    debts = Debts(collection=collection)
    payments, expenses = None, None
    if person := request.args.get('person', ''):
        payments = debts.get_payments(person)
        expenses = debts.get_expenses(person)
    kwargs = {'collection': collection,
              '_debts': debts.get_debts(),
              'payments': payments,
              'expenses': expenses}
    return render_template('result.html', **kwargs)

# TODO: add home link to each page -> make some design
# TODO: try to make dockerfile smaller size
# ------------- DEBUG ----------------
# @app.route('/<collection>/clear')
# def debts_clear(collection):
#     debts = Debts(collection=collection)
#     debts.clear()
#     return 'DEBUG: Database cleared'


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)
