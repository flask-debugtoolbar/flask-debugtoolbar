# Run using: `FLASK_ENV=development flask run`

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
#app.config['DEBUG_TB_PANELS'] = (
#    'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
#    'flask_debugtoolbar.panels.logger.LoggingPanel',
#    'flask_debugtoolbar.panels.timer.TimerDebugPanel',
#)
#app.config['DEBUG_TB_HOSTS'] = ('127.0.0.1', '::1' )
app.config['SECRET_KEY'] = 'asd'

# TODO: This can be removed once flask_sqlalchemy 3.0 ships
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

toolbar = DebugToolbarExtension(app)


class ExampleModel(db.Model):
    __tablename__ = 'examples'
    value = db.Column(db.String(100), primary_key=True)


@app.before_first_request
def setup():
    db.create_all()


@app.route('/')
def index():
    app.logger.info("Hello there")
    ExampleModel.query.get(1)
    return render_template('index.html')


@app.route('/redirect')
def redirect_example():
    response = redirect(url_for('index'))
    response.set_cookie('test_cookie', '1')
    return response
