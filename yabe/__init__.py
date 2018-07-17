from flask import (Flask, request)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS

from config import Config

import os, logging

yabe = Flask(__name__)
CORS(yabe)
yabe.config.from_object(Config)
db = SQLAlchemy(yabe)
migrate = Migrate(yabe, db)
auth = HTTPBasicAuth()

from yabe import views, models
from yabe.models import Post, Tag


@yabe.shell_context_processor
def make_shell_context():
    return {'db': db, 'Post': Post, 'Tag': Tag}
