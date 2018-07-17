from yabe import db, yabe
from datetime import datetime
from flask import jsonify
from passlib.apps import custom_app_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          SignatureExpired, BadSignature)

r_tags = db.Table('r_tags',
                  db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                  db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

r_pages = db.Table('r_pages',
                   db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                   db.Column('page_id', db.Integer, db.ForeignKey('page.id')))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Tag {}> {}'.format(self.id, self.content)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    summary = db.Column(db.Text)

    def __repr__(self):
        return '<Category {}> {}'.format(self.id, self.title)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64))
    content = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Comment {} of Page {}> {}<{}>: {}'.format(
            self.id, self.post_id, self.username, self.email, self.content)

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'username': self.username,
            'email': self.email,
            'content': self.content
        }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    post_time = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    tags = db.relationship(
        'Tag',
        secondary=r_tags,
        backref=db.backref('posts', lazy='dynamic'),
        lazy='dynamic')

    content = db.Column(db.Text)
    content_uri = db.Column(db.String(128))

    draft = db.Column(db.Boolean)
    invisible = db.Column(db.Boolean)
    protected = db.Column(db.Boolean)
    password = db.Column(db.String(64))  # Use md5

    def add_tag(self, tag):
        if not self.has_tag(tag):
            self.tags.append(tag)
            return self

    def remove_tag(self, tag):
        if self.has_tag(tag):
            self.tags.remove(tag)
            return self

    def add_comment(self, comment):
        if not self.has_comment(comment):
            self.comments.append(comment)
            return self

    def remove_comment(self, comment):
        if self.has_comment(comment):
            self.comments.remove(comment)
            return self

    def has_comment(self, comment):
        return self.comments.filter(Comment.id == comment.id).count() > 0

    def has_tag(self, tag):
        return self.tags.filter(r_tags.c.tag_id == tag.id).count() > 0

    def get_tags_content(self):
        return list(map(lambda tag: tag.content, self.tags.all()))

    def __repr__(self):
        return '<Post {}> {}'.format(self.id, self.title)

    def to_dict(self, summary=False):
        result = {'id': self.id}
        if not self.invisible:
            result = dict(
                result, **{
                    'title': self.title,
                    'post_time': self.post_time,
                    'category_id': self.category_id,
                    'tags': [(tag.id, tag.content) for tag in self.tags.all()],
                    'draft': self.draft,
                    'invisible': self.invisible,
                    'protected': self.protected
                })
            if not self.protected:
                if summary:
                    result = dict(
                        result, **{
                            'content':
                            self.content,
                            'comments':
                            [comment.to_dict() for comment in self.comments]
                        })
        return result

    def to_json(self, summary=True):
        return jsonify(self.to_dict(summary))


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))

    posts = db.relationship(
        'Post',
        secondary=r_pages,
        backref=db.backref('pages', lazy='dynamic'),
        lazy='dynamic')

    def add_post(self, post):
        if not self.has_post(post):
            self.posts.append(post)
            return self

    def remove_post(self, post):
        if not self.has_post(post):
            self.posts.remove(post)
            return self

    def has_post(self, post):
        return self.posts.filter(r_pages.c.post_id == post.id).count() > 0

    def __repr__(self):
        return '<Page {}> {} post(s)'.format(self.id, self.posts.count())


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(128))
    has_power = db.Column(db.Boolean)

    def set_passwd(self, passwd):
        self.password = custom_app_context.encrypt(passwd)

    def chk_passwd(self, passwd):
        return custom_app_context.verify(passwd, self.password)

    def get_token(self, expiration=3600):
        s = Serializer(yabe.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def chk_token(token):
        s = Serializer(yabe.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return Admin.query.get(data['id'])
