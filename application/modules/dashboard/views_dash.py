__author__ = 'Ronald'


from ...modules import *
from ..user.models_user import Participation
from ..parametre.models_parametre import Parametre

# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)
prefix = Blueprint('dash', __name__)


@prefix.route('')
def index():
    menu = 'dash'

    if not Parametre.query().get():
        return redirect(url_for('parametre.index'))

    search = False
    q = request.args.get('q')
    if q:
        search = True
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    list_part = Participation.query().order(-Participation.pourcentage)
    pagination = Pagination(css_framework='bootstrap3', page=page, total=list_part.count(), search=search, record_name='users')

    if list_part.count() > 10:
        if page == 1:
            offset = 0
        else:
            page -= 1
            offset = page * 10
        users = list_part.fetch(limit=10, offset=offset)

    return render_template('home/dash.html', **locals())