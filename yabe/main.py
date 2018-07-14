from flask import (Blueprint, render_template, request)

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def router_index():
    return 'Hello World, youra.'
