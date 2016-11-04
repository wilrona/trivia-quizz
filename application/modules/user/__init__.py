__author__ = 'wilrona'


from views_user import *

app.register_blueprint(prefix, url_prefix='/user')
app.register_blueprint(prefix_home)