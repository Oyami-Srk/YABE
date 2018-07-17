from flask import (Blueprint, render_template, request)
from .models import Post
from yabe import db

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'], defaults={'path': ''})
@main.route('/<path:path>')
def router_index(path):
    return render_template('index.html')


@main.route('/post/<int:id>')
def get_post(id):
    return str(Post.query.filter_by(id=id).first_or_404().content)
