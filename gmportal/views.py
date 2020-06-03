from flask import render_template, request, Blueprint

startBP=Blueprint('startBP',__name__)


@startBP.route('/')
def index():
    # more to come
    return render_template('index.html')