from flask import Blueprint

# Create a variable app_views
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
