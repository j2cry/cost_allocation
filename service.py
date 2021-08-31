from flask import Flask, render_template, request, redirect
from debts import Debts

app = Flask(__name__)


@app.route('/<collection>', methods=['POST', 'GET'])
def debts_service(collection):
    """
        :param collection: mongo database collection name """
    if request.method == 'POST':        # add record to database
        debts = Debts(collection=collection)
        record = dict(request.form)
        record['sharers'] = record.get('sharers').split()
        debts.push(record)

    debts = Debts(collection=collection)
    return render_template('data.html', collection=collection, records=debts.get_all())


@app.route('/<collection>/result', methods=['POST'])
def debts_result(collection):
    debts = Debts(collection=collection)
    # TODO: html template for result output
    return str(debts.get_debts())


@app.route('/<collection>/remove')
def debts_remove_item(collection):
    debts = Debts(collection=collection)
    if _id := request.args.get('_id', None):
        debts.remove(_id)
    return redirect(f'/{collection}')


# ------------- DEBUG ----------------
@app.route('/<collection>/clear')
def debts_clear(collection):
    debts = Debts(collection=collection)
    debts.clear()
    return 'DEBUG: Database cleared'


if __name__ == '__main__':
    app.run()
