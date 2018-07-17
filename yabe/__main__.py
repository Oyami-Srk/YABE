from yabe import yabe, db
from .models import Post
import os
import click


@click.group()
def cli():
    """ Yabe CLI """
    pass


@cli.command()
def drop_all_database():
    db.session.remove()
    db.drop_all()


@cli.command()
def create_all_database():
    db.create_all()


@cli.command()
def fill_test_data():
    p1 = Post(
        title='Test Post 1',
        content=
        '<h1>Hello World!</h1><p/>This is a test post, remove it after development<p/>YABE - Yet Another Blog Engine'
    )
    db.session.add(p1)
    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    cli()
