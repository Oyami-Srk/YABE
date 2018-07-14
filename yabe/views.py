from yabe import yabe

from .main import main

yabe.register_blueprint(main, url_prefix='/')
