from flask import Flask, render_template, request, redirect
from waitress import serve
from debts import Debts

app = Flask(__name__)


@app.route('/<collection>', methods=['POST', 'GET'])
def debts_service(collection):
    """ Show HTML interface
        :param collection: mongo database collection name """
    debts = Debts(collection=collection)
    return render_template('data.html', collection=collection, records=debts.get_all())


@app.route('/<collection>/add', methods=['POST'])
def debts_add_item(collection):
    """ Add record to database and redirect to main interface
        :param collection: mongo database collection name """
    debts = Debts(collection=collection)
    record = dict(request.form)
    record['sharers'] = record.get('sharers').split()
    debts.push(record)
    return redirect(f'/{collection}')


@app.route('/<collection>/remove')
def debts_remove_item(collection):
    """ Remove record from database and redirect to main interface
        :param collection: mongo database collection name """
    debts = Debts(collection=collection)
    if _id := request.args.get('_id', None):
        debts.remove(_id)
    return redirect(f'/{collection}')


@app.route('/<collection>/result', methods=['POST'])
def debts_result(collection):
    """ Show result
        :param collection: mongo database collection name """
    debts = Debts(collection=collection)
    # TODO: html template for result output
    return render_template('result.html', collection=collection, _debts=debts.get_debts())


# ------------- DEBUG ----------------
# @app.route('/<collection>/clear')
# def debts_clear(collection):
#     debts = Debts(collection=collection)
#     debts.clear()
#     return 'DEBUG: Database cleared'


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)
    # app.run(host='0.0.0.0')
