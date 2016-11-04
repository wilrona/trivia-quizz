__author__ = 'Ronald'


from ...modules import *
from models_parametre import Parametre

# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)
prefix = Blueprint('parametre', __name__)


@prefix.route('', methods=['POST', 'GET'])
def index():
    menu = 'parametre'

    current_param = Parametre.query().get()

    if request.method == 'POST':

        participation = request.form['participation']
        question = request.form['question']
        date = function.date_convert(request.form['date'])

        if not current_param:
            current_param = Parametre()

        current_param.nbr_participation = int(participation)
        current_param.nbr_question = int(question)
        current_param.date_event = date
        current_param.put()

    return render_template('parametre/index.html', **locals())
