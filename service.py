from flask import Flask, render_template, request
from waitress import serve
import configparser
import pathlib
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
        'sharer_template': render_template('sharer.jinja2')
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
    sharers = ['foo', 'boo', 'bar']
    return render_page('calc.jinja2', notebook=name, sharers=sharers)


@app.route(SERVICE_URL.joinpath('<name>', 'clear').as_posix())
def clear(name):
    debts = Debts(**mongo_params, collection=name)
    debts.clear()
    return 'notebook cleared'


@app.route(SERVICE_URL.joinpath('api').as_posix(), methods=['POST'])
def api():
    """ Receive json request, process and send response """
    action = request.json.pop('action', '')
    name = request.json.pop('name', '')
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
    else:
        resp = {}
    return resp

# @app.route(f'{settings.SERVICE_PATH}/<collection>/result', methods=['GET', 'POST'])
# def debts_result(collection):
#     """ Show result
#         :param collection: mongo database collection name """
#     debts = Debts(collection=collection)
#     payments, expenses = None, None
#     if person := request.args.get('person', ''):
#         payments = debts.get_payments(person)
#         expenses = debts.get_expenses(person)
#     params = {'home': settings.SERVICE_PATH,
#               'collection': collection,
#               '_debts': debts.get_debts(),
#               'person': person,
#               'payments': payments,
#               'expenses': expenses}
#     return render_template('index.jinja2', page='result.html', **params)


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=int(config['URLS']['port']))
