from flask import render_template, request, Blueprint

home = Blueprint('home', __name__)


@home.route("/")
@home.route("/home")
def homepage():
    return render_template('home.html')


@home.route("/about")
def about():
    return render_template('about.html', title='About')


@home.route("/wip")
def wip():
    return render_template('wip.html')
