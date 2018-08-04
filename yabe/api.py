from flask import (Blueprint, render_template, request, current_app, jsonify,
                   abort, g)
from .models import Post, Admin
from yabe import db, yabe, auth

api = Blueprint('api', __name__)


@api.route('/get_all_posts')
@auth.login_required
def get_all_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.post_time.desc()).paginate(
        page, per_page=yabe.config['POSTS_PER_PAGE'], error_out=False)
    posts = [post for post in pagination.items if post.draft is not True]
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_all_posts', page=page - 1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_all_posts', page=page + 1, _external=True)

    summary = request.args.get('summary', False, type=bool)
    print(list(map(lambda x: x.draft, [post for post in pagination.items])))
    return jsonify({
        'posts': [post.to_dict(summary) for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/get_post')
@auth.login_required
def get_post():
    post_id = request.args.get('post_id', 0, type=int)
    post = Post.query.get_or_404(post_id)
    print(post.to_json())
    return post.to_json()


@api.route('/create_user', methods=['POST'])
def create_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
    if Admin.query.filter_by(username=username).count() > 0:
        abort(400)

    new_admin = Admin(username=username)
    new_admin.set_passwd(password)
    db.session.add(new_admin)
    db.session.commit()
    print(new_admin)
    db.session.close()
    return jsonify({'username': new_admin.username})


@auth.verify_password
def verify_password(username_or_token, password):
    if request.path == '/api/login':
        admin = Admin.query.filter_by(username=username_or_token).first()
        if not admin or not admin.chk_passwd(password):
            return False
    else:
        admin = Admin.chk_token(username_or_token)
        if not admin:
            return False
    g.admin = admin
    return True


@api.route('/login')
@auth.login_required
def get_token():
    print(g.admin.get_token())
    token = g.admin.get_token(request.args.get('expiration', 3600, type=int))
    return jsonify(token.decode('utf-8'))
