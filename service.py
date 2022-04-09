from flask import Flask, render_template, request, redirect
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
DUPLICATES = bool(config['MONGO']['duplicates'])

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


@app.route(SERVICE_URL.joinpath('api').as_posix(), methods=['POST'])
def api():
    """ Receive json request, process and send response """
    print(request.json)
    # TODO: придумай формат сообщений
    action = request.json.get('action', '')
    name = request.json.get('name', '')
    if not (action and name):
        return {'error': 'bad_request'}

    if action == 'select':
        debts = Debts(**mongo_params, collection=name)
        resp = dict(enumerate(debts.get_all(), 1))
    elif action == 'update':
        resp = {}
    else:
        resp = {}
    return resp

# @app.route(f'{settings.SERVICE_PATH}/<collection>', methods=['POST', 'GET'])
# def debts_service(collection):
#     """ Show HTML interface
#         :param collection: mongo database collection name """
#     debts = Debts(collection=collection)
#     settings.MONGO_COLLECTION = collection
#     params = {'home': settings.SERVICE_PATH,
#               'collection': collection,
#               'forced': settings.ALLOW_DUPLICATES,
#               'records': enumerate(debts.get_all(), 1)}
#     return render_template('index.jinja2', page='data.jinja2', **params)
#
#
# @app.route(f'{settings.SERVICE_PATH}/<collection>/add', methods=['POST'])
# def debts_add_item(collection):
#     """ Add record to database and redirect to main interface
#         :param collection: mongo database collection name """
#     debts = Debts(collection=collection)
#     record = dict(request.form)
#     settings.ALLOW_DUPLICATES = bool(record.pop('forced', 0))
#     record['sharers'] = record.get('sharers').split()
#     debts.push(record, forced=settings.ALLOW_DUPLICATES)
#     return redirect(f'{settings.SERVICE_PATH}/{collection}')
#
#
# @app.route(f'{settings.SERVICE_PATH}/<collection>/remove')
# def debts_remove_item(collection):
#     """ Remove record from database and redirect to main interface
#         :param collection: mongo database collection name """
#     debts = Debts(collection=collection)
#     if _id := request.args.get('_id', None):
#         debts.remove(_id)
#     return redirect(f'{settings.SERVICE_PATH}/{collection}')
#
#
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
#
#
# @app.route(f'{settings.SERVICE_PATH}/about')
# def debts_about():
#     params = {'home': settings.SERVICE_PATH,
#               'collection': settings.MONGO_COLLECTION}
#     return render_template('index.jinja2', page='faq.jinja2', **params)


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=int(config['URLS']['port']))
