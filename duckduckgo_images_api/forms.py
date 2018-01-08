"""Forms module."""
from flask_wtf import FlaskForm
from wtforms import validators
import wtforms

from duckduckgo_images_api import api


class IndexForm(FlaskForm):
    """Form for index."""
    query = wtforms.StringField('query',  [validators.Required()])
    p_value = wtforms.StringField('p value', default=api.DEFAULT_P_VALUE)
