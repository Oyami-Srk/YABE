from yabe import yabe

from .main import main
from .api import api

yabe.register_blueprint(main, url_prefix='/')
yabe.register_blueprint(api, url_prefix='/api')
