"""module for admin."""
from math import ceil

from flask import request, flash
from flask_admin import AdminIndexView, expose
from flask_paginate import Pagination, get_page_parameter
import structlog

from duckduckgo_images_api import forms, models


log = structlog.getLogger(__name__)


class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        form = forms.IndexForm(request.args)
        page = request.args.get(get_page_parameter(), type=int, default=1)
        query = form.query.data
        p_value = form.p_value.data

        template_kwargs = {
            'entry': None,
            'query': query,
            'form': form,
        }
        pagination_kwargs = {
            'page': page,
            'show_single_page': False,
            'bs_version': 3,
        }
        if query:
            try:
                entry, is_created = models.Search.get_or_create_from_query(
                    query, page=page, p_value=p_value)
            except ValueError as e:
                log.warning('ValueError', s=e)
                flash(e)
                template_kwargs['pagination'] = Pagination(**pagination_kwargs)
                return self.render('ddg_images_api/index.html', **template_kwargs)

            if is_created:
                models.db.session.add(entry)
                models.db.session.commit()
            template_kwargs['entry'] = entry
            pagination_kwargs['total'] = models.Search.query.join(  # total search result
                models.Search.search_results
            ).filter(
                models.Search.search_query == query,
                models.Search.p_value == p_value
            ).count()
            if pagination_kwargs['total'] == 0:
                msg = 'No result found for query:{}'.format(query)
                log.warning(msg)
                flash(msg)
                template_kwargs['pagination'] = Pagination(**pagination_kwargs)
                return self.render('ddg_images_api/index.html', **template_kwargs)

            total_page = models.Search.query.filter(
                models.Search.search_query == query,
                models.Search.p_value == p_value
            ).count()
            log.debug('total page', value=total_page)

            pagination_kwargs['per_page'] = int(ceil(pagination_kwargs['total'] / total_page))
        log.debug('pagination kwargs', **pagination_kwargs)
        template_kwargs['pagination'] = Pagination(**pagination_kwargs)
        return self.render('ddg_images_api/index.html', **template_kwargs)
