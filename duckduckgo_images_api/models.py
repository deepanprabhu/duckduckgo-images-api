"""Model module."""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TIMESTAMP
from sqlalchemy_utils.types import URLType

from duckduckgo_images_api import api


db = SQLAlchemy()

search_results = db.Table(  # pylint: disable=invalid-name
    'search_results',
    db.Column('search_id', db.Integer, db.ForeignKey('search.id'), primary_key=True),
    db.Column('search_result_id', db.Integer, db.ForeignKey('search_result.id'), primary_key=True)
)
image_tags = db.Table(
    'image_tags',
    db.Column('image_url_value', db.Integer, db.ForeignKey('image_url.value'), primary_key=True),
    db.Column('tag_full_name', db.Integer, db.ForeignKey('tag.full_name'), primary_key=True)
)


class Search(db.Model):
    """search model."""
    id = db.Column(db.Integer(), primary_key=True)
    search_query = db.Column(db.String(), nullable=False)
    page = db.Column(db.Integer(), nullable=False)
    vqd = db.Column(db.String())
    p_value = db.Column(db.String(), nullable=False)
    next_request_url = db.Column(URLType)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        """Get string representation of obj."""
        return "<Search {0.id} query:'{0.search_query}' page:{0.page} vqd:{1} p value:{0.p_value}>".format(
            self, self.shorted_vqd)

    @property
    def shorted_vqd(self):
        max_len = 7
        return (self.vqd[:max_len] + '...') if len(self.vqd) > max_len else self.vqd

    @staticmethod
    def get_or_create_from_query(query, page=1, use_cache=True, p_value=None):
        """Get or create from query."""
        p_value = p_value if p_value else api.DEFAULT_P_VALUE
        kwargs = {'search_query': query, 'page': page, 'p_value': p_value}
        model, is_model_created = get_or_create(db.session, Search, **kwargs)
        if not is_model_created:
            return model, is_model_created
        if page == 1:
            result_gen = api.search(query, p_value=p_value)
            result = next(result_gen)
        elif page > 1:
            # ppsm = previous page search model
            ppsm, ppsm_created = Search.get_or_create_from_query(query, page=page-1, p_value=p_value)
            if ppsm_created:
                db.session.add(ppsm)
                db.session.commit()
            if not ppsm.next_request_url:
                raise ValueError('No "next request url" found.')
            result = next(api.search(
                query, vqd=ppsm.vqd, request_url=ppsm.next_request_url, p_value=p_value
            ))
        with db.session.no_autoflush:
            search_result_models_sets = list(SearchResult.get_or_create_from_json_data(result['json_data']))
        search_result_models = [x[0] for x in search_result_models_sets]
        model.search_results.extend(search_result_models)
        model.vqd = result['vqd']
        model.next_request_url = result['next_request_url']
        return model, is_model_created


class SearchResult(db.Model):
    """Search result model."""
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(URLType, db.ForeignKey('image_url.value'), nullable=False)
    image_url_model = db.relationship('ImageUrl', backref=('search_results'))
    thumbnail_url = db.Column(URLType)
    title = db.Column(db.String())
    url = db.Column(URLType)
    source = db.Column(db.String())
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    search_models = db.relationship(
        'Search', secondary=search_results, lazy='subquery', backref=db.backref('search_results', lazy=True))

    @staticmethod
    def get_or_create_from_json_data(json_data):
        """Get or create from json data."""
        for data in json_data['results']:
            height = int(data['height'])
            width = int(data['width'])
            image_url_kwargs = {
                'value': data['image'],
                'height': height,
                'width': width,
            }
            image_url, _ = get_or_create(db.session, ImageUrl, **image_url_kwargs)
            search_result_model_kwargs = {
                'image_url': image_url.value,
                'thumbnail_url': data['thumbnail'],
                'title': data['title'],
                'url': data['url'],
                'source': data['source'],
            }
            search_result_model, is_created = get_or_create(db.session, SearchResult, **search_result_model_kwargs)
            yield search_result_model, is_created


class ImageUrl(db.Model):
    value = db.Column(URLType, primary_key=True)
    height = db.Column(db.Integer())
    width = db.Column(db.Integer())
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    tags = db.relationship('Tag', secondary=image_tags, lazy='subquery', backref=db.backref('image_urls', lazy=True))

    @property
    def size(self):
        return '{}x{}'.format(self.width, self.height)


class Tag(db.Model):
    """Tag model."""
    full_name = db.Column(db.String, primary_key=True)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    @property
    def name(self):
        """Get tag name."""
        if ':' in self.full_name:
            return self.full_name.split(':', 1)[1]
        return self.full_name

    @property
    def namespace(self):
        """Get tag namespace."""
        if ':' in self.full_name:
            return self.full_name.split(':', 1)[0]


def get_or_create(session, model, **kwargs):
    """Creates an object or returns the object if exists."""
    instance = session.query(model).filter_by(**kwargs).first()
    created = False
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        created = True
    return instance, created
