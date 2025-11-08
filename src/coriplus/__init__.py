'''
Cori+
=====

The root module of the package.
This module also contains very basic web hooks, such as robots.txt.

For the website hooks, see `app.website`.
For the AJAX hook, see `app.ajax`.
For public API, see `app.api`.
For report pages, see `app.reports`.
For site administration, see `app.admin`.
For template filters, see `app.filters`.
For the database models, see `app.models`.
For other, see `app.utils`.
'''

from flask import (
    Flask, g, jsonify, render_template, request,
    send_from_directory, __version__ as flask_version)
import os, sys
from flask_login import LoginManager
from flask_wtf import CSRFProtect
import dotenv
import logging

__version__ = '0.10.0-dev44'

# we want to support Python 3.10+ only.
# Python 2 has too many caveats.
# Python <=3.9 has harder type support.
if sys.version_info[0:2] < (3, 10):
    raise RuntimeError('Python 3.10+ required')

BASEDIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
os.chdir(BASEDIR)

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

login_manager = LoginManager(app)

CSRFProtect(app)

from .models import *

from .utils import *

from .filters import *

### WEB ###

login_manager.login_view = 'website.login'

@app.before_request
def before_request():
    g.db = database
    try:
        g.db.connect()
    except OperationalError:
        logger.error('database connected twice.\n')

@app.after_request
def after_request(response):
    try:
        g.db.close()
    except Exception:
        logger.error('database closed twice')
    return response

@app.context_processor
def _inject_variables():
    return {
        'site_name': os.environ.get('APP_NAME', 'Cori+'),
        'locations': locations,
        'inline_svg': inline_svg
    }

@login_manager.user_loader
def _inject_user(userid):
    return User[userid]

@app.errorhandler(403)
def error_403(body):
    return render_template('403.html'), 403

@app.errorhandler(404)
def error_404(body):
    return render_template('404.html'), 404
    
@app.route('/favicon.ico')
def favicon_ico():
    return send_from_directory(BASEDIR, 'src/favicon.ico')

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(BASEDIR, 'src/robots.txt')

@app.route('/uploads/<id>.<type>')
def uploads(id, type='jpg'):
    return send_from_directory(UPLOAD_DIRECTORY, id + '.' + type)

@app.route('/get_access_token', methods=['POST'])
def send_access_token():
    try:
        data = request.get_json(True)
        try:
            user = User.get(
                (User.username == data['username']) & 
                (User.password == pwdhash(data['password'])))
        except User.DoesNotExist:
            return jsonify({
                'message': 'Invalid username or password',
                'login_correct': False, 
                'status': 'ok'
            })
        if user.is_disabled == 1:
            user.is_disabled = 0
        elif user.is_disabled == 2:
            return jsonify({
                'message': 'Your account has been disabled by violating our Terms.',
                'login_correct': False, 
                'status': 'ok'
            })
        return jsonify({
            'token': generate_access_token(user),
            'login_correct': True,
            'status': 'ok'
        })
    except Exception:
        sys.excepthook(*sys.exc_info())
        return jsonify({
            'message': 'An unknown error has occurred.',
            'status': 'fail'
        })

from .website import bp
app.register_blueprint(bp)

from .ajax import bp
app.register_blueprint(bp)

from .api import bp
app.register_blueprint(bp)

from .reports import bp
app.register_blueprint(bp)

from .admin import bp
app.register_blueprint(bp)
