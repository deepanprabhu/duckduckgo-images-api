#!/usr/bin/python3
"""Server module."""
from logging.handlers import TimedRotatingFileHandler
import logging
import os
import tempfile

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import click
import flask

from duckduckgo_images_api import models, admin


app = flask.Flask(__name__)  # pylint: disable=invalid-name


class SearchResultView(ModelView):
    def _thumbnail_url_formatter(view, context, model, name):
        return flask.Markup('<a href="{1}"><img style="max-height: 100px; max-width: 100px;" src="{0}"></a>'.format(
            model.thumbnail_url,
            flask.url_for('searchresult.edit_view', id=model.id)
        ))

    def _title_formatter(view, context, model, name):
        return flask.Markup('{0}<br><a href="{1}">{1}</a><br>Image URL: <a href="{2}">{2}</a>'.format(
            model.title, model.url, model.image_url
        ))

    column_exclude_list = ['url', 'image_url_model']
    column_formatters = {
       'thumbnail_url': _thumbnail_url_formatter,
       'title': _title_formatter,
    }


class ImageUrlView(ModelView):

    def _value_formatter(view, context, model, name):
        search_result = next(iter(model.search_results or []), None)
        thumbnail_url = search_result.thumbnail_url if search_result else None
        template = '<a href="{1}"><img src="{0}"></a><br>{2} <a href="{3}">link</a>'
        return flask.Markup(template.format(
            thumbnail_url,
            flask.url_for('imageurl.edit_view', id=model.value.replace('.', '..')),
            model.size, model.value
        ))

    column_exclude_list = ('width', 'height')
    column_display_pk = True
    column_formatters = {
       'value': _value_formatter,
    }
    edit_template = 'ddg_images_api/imageurl_edit.html'


class SearchView(ModelView):
    def _search_query_formatter(view, context, model, name):
        return flask.Markup('<a href="{}">{}</a>'.format(
            flask.url_for('admin.index', query=model.search_query, p_value=model.p_value),
            model.search_query
        ))

    def _page_formatter(view, context, model, name):
        return flask.Markup('<a href="{}">{}</a>'.format(
            flask.url_for('admin.index', query=model.search_query, p_value=model.p_value, page=model.page),
            model.page
        ))

    def _vqd_formatter(view, context, model, name):
        return flask.Markup(model.shorted_vqd)

    column_formatters = {
       'search_query': _search_query_formatter,
       'page': _page_formatter,
       'vqd': _vqd_formatter,
    }


@click.group()
def cli():
    """CLI command."""
    pass


@cli.command()
@click.option("-h", "--host", default="127.0.0.1", type=str)
@click.option("-p", "--port", default=5000, type=int)
@click.option("-d", "--debug", is_flag=True)
@click.option("-r", "--reloader", is_flag=True)
@click.option("--threaded", is_flag=True)
@click.option("--testing", is_flag=True)
@click.option("--db-path", default='ddg_images_api.db', type=click.Path())
def run(
        host='127.0.0.1', port=5000, debug=False, reloader=False, threaded=False, testing=False,
        db_path='ddg_images_api.db'
):
    """Run the application server."""
    if reloader:
        app.jinja_env.auto_reload = True
        app.config["TEMPLATES_AUTO_RELOAD"] = True
    # logging
    directory = 'log'
    if not os.path.exists(directory):
        os.makedirs(directory)
    default_log_file = os.path.join(directory, 'ddg_images_api.log')
    file_handler = TimedRotatingFileHandler(default_log_file, 'midnight')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
    app.logger.addHandler(file_handler)
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    app_admin = Admin(
        app, name='Duckduckgo images api', template_mode='bootstrap3',
        index_view=admin.HomeView(name='Home', template='ddg_images_api/index.html', url='/')
    )
    list(map(lambda x: app_admin.add_view(ModelView(x, models.db.session)), [
        models.Tag,
    ]))
    app_admin.add_view(SearchResultView(models.SearchResult, models.db.session))
    app_admin.add_view(ImageUrlView(models.ImageUrl, models.db.session))
    app_admin.add_view(SearchView(models.Search, models.db.session))

    if debug:
        app.config['DEBUG'] = True
    if testing:
        app.config['TESTING'] = True
    # app config
    app.config['SECRET_KEY'] = os.getenv('DDG_SERVER_SECRET_KEY') or \
        os.urandom(24)
    app.logger.debug('db path: {}'.format(os.path.realpath(db_path)))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.realpath(db_path))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # setting before running app
    models.db.init_app(app)
    app.app_context().push()
    models.db.create_all()
    # app run
    app.run(
        host=host, port=port,
        debug=debug, use_debugger=debug,
        use_reloader=reloader,
        threaded=threaded
    )


if __name__ == '__main__':
    cli()
