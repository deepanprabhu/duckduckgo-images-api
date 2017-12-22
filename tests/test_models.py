"""test module query."""
from duckduckgo_images_api import models
from flask import Flask
import vcr
import pytest


@pytest.fixture()
def tmp_db(tmpdir):
    """Return temporary db."""
    app = Flask(__name__)
    tmp_db_path = tmpdir.join('temp.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + tmp_db_path.strpath
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    models.db.init_app(app)
    app.app_context().push()
    models.db.create_all()
    return models.db


@pytest.mark.no_travis
@vcr.use_cassette('cassette/test_get_first_page_from_query.yaml', record_mode='new_episodes')
def test_get_first_page_from_query(tmp_db):
    query = 'red image'
    m, is_created = models.Search.get_or_create_from_query(query)
    assert is_created
    assert len(m.search_results) > 0
    models.db.session.add(m)
    models.db.session.commit()
    vqd = m.vqd
    next_request_url = m.next_request_url
    assert vqd
    assert next_request_url
    m2, is_created = models.Search.get_or_create_from_query(query)
    assert not is_created
    assert vqd == m2.vqd
    assert next_request_url == m2.next_request_url


@pytest.mark.no_travis
@vcr.use_cassette('cassette/test_get_first_and_second_page_from_query.yaml', record_mode='new_episodes')
def test_get_first_and_second_page_from_query(tmp_db):
    query = 'red image'
    m_p1, _ = models.Search.get_or_create_from_query(query)
    models.db.session.add(m_p1)
    models.db.session.commit()
    m_p2, _ = models.Search.get_or_create_from_query(query, page=2)
    assert m_p2.page == 2
    assert m_p2.vqd == m_p1.vqd
    assert len(m_p2.search_results) > 0


@pytest.mark.no_travis
@vcr.use_cassette('cassette/test_get_direct_third_page_from_query.yaml', record_mode='new_episodes')
def test_get_direct_third_page_from_query(tmp_db):
    query = 'red image'
    m_p3, _ = models.Search.get_or_create_from_query(query, page=3)
    assert m_p3.page == 3
    assert len(m_p3.search_results) > 0
    page_models = models.db.session.query(models.Search).all()
    assert len(page_models) == 3
