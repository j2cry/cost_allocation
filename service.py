from flask import Flask, render_template, request
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

    # TODO: html template for records output
    # TODO: feature for records deleting
    return render_template('data.html', collection=collection)


@app.route('/<collection>/result', methods=['POST'])
def debts_result(collection):
    debts = Debts(collection=collection)
    print(debts.get_debts())
    # TODO: html template for result output
    return str(debts.get_debts())


# ------------- DEBUG ----------------
@app.route('/<collection>/clear')
def debts_clear(collection):
    debts = Debts(collection=collection)
    debts.clear()
    return 'DEBUG: Database cleared'


@app.route('/<collection>/all')
def debts_all(collection):
    debts = Debts(collection=collection)
    debts.get_all()
    return 'DEBUG: get all records'


if __name__ == '__main__':
    app.run()
