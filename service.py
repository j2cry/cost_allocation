import pandas as pd
import configparser
import pathlib
from flask import Flask, render_template, request
from waitress import serve
from debts import Debts


config = configparser.ConfigParser()
config.read('conf.d/default.cnf')
SERVICE_URL = pathlib.Path('/', config['URLS']['service'])
mongo_params = {
    'server': config['MONGO']['server'],
    'database': config['MONGO']['database'],
}
FORCE_PUSH = bool(config['MONGO']['duplicates'])

app = Flask(__name__, static_url_path=SERVICE_URL.joinpath('static').as_posix())


def render_page(content_template=None, **kwargs):
    page_params = {
        'home_url': SERVICE_URL.as_posix(),
        'row_template': render_template('data_row.jinja2'),
        'sharer_template': render_template('sharer.jinja2'),
        'debug': config['URLS']['debug']
    }
    return render_template('index.jinja2', content=content_template, params=page_params, **kwargs)


@app.route(SERVICE_URL.as_posix())
def index():
    """ Welcome page """
    return render_page('welcome.jinja2')


@app.route(SERVICE_URL.joinpath('about').as_posix())
def about():
    """ About/FAQ page """
    return render_page('faq.jinja2')


@app.route(SERVICE_URL.joinpath('<name>').as_posix())
def notebook(name):
    """ Data editor page """
    return render_page('data.jinja2', notebook=name)


@app.route(SERVICE_URL.joinpath('<name>', 'calc').as_posix())
def calc(name):
    """ Calculations page """
    debts = Debts(**mongo_params, collection=name)
    sharers = debts.get_sharers()
    common = debts.get_debts()
    return render_page('calc.jinja2', notebook=name, sharers=sharers, common=common)


# @app.route(SERVICE_URL.joinpath('<name>', 'clear').as_posix())
# def clear(name):
#     debts = Debts(**mongo_params, collection=name)
#     debts.clear()
#     return 'notebook cleared'


@app.route(SERVICE_URL.joinpath('api').as_posix(), methods=['POST'])
def api():
    """ Receive json request, process and send response """
    action = request.json.get('action', '')
    name = request.json.get('name', '')
    if not (action and name):
        return {'error': 'bad_request'}
    debts = Debts(**mongo_params, collection=name)

    if action == 'select':
        docs, sharers = debts.get_all()
        for doc in docs:
            doc['_id'] = str(doc['_id'])
        resp = {'sharers': sharers,
                'docs': docs}
    elif action == 'update':
        debts.remove(request.json['remove'])
        inserted_ids = debts.update(docs=request.json['docs'], sharers=request.json['sharers'])
        resp = {'ids': inserted_ids}
    elif action == 'calc':
        person = request.json.get('person')
        expenses = debts.get_expenses(person)
        payments = debts.get_payments(person)
        resp = pd.concat([expenses, payments], axis=1).fillna(0).T.to_dict()
        print(resp)
    else:
        resp = {}
    return resp


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=int(config['URLS']['port']))
