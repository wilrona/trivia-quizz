__author__ = 'wilrona'

from ...modules import *
from application import login_manager
from models_user import Users, ndb, Participation
from ..parametre.models_parametre import Parametre
from ..question.models_question import Reponse, Question

# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)
prefix = Blueprint('user', __name__)
prefix_home = Blueprint('home', __name__)


@login_manager.user_loader
def load_user(userid):
    return Users.get_by_id(userid)


@prefix_home.route('/')
def home():
    link = 'home'

    time_zones = pytz.timezone('Africa/Douala')
    date_auto_nows = datetime.datetime.now(time_zones)
    param = Parametre.query().get()

    inscription = True
    if param and param.date_event and param.date_event <= function.date_convert(date_auto_nows):
        inscription = False

    fin = False
    if param and param.date_event and param.date_event < function.date_convert(date_auto_nows):
        fin = True

    return render_template('home/index.html', **locals())


@prefix_home.route('/principe')
def principe():
    link = 'principe'

    return render_template('home/principe.html', **locals())


@prefix.route('/logout')
def logout():
    change = None

    if 'user_id' in session:
        UserLogout = Users.get_by_id(int(session.get('user_id')))
        UserLogout.logged = False
        change = UserLogout.put()

    if change:
        session.pop('user_id')

    return redirect(url_for('home.home'))


@prefix.route('')
def index():
    menu = 'user'

    search = False
    q = request.args.get('q')
    if q:
        q = ''.join(q.split(' '))
        search = True
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    users = Users.query()
    if search:
        list_user = users
        users = []
        for user in list_user:
            find_user = function.find(str(user.matricule), str(q))
            if find_user:
                users.append(user)

        pagination = Pagination(css_framework='bootstrap3', page=page, total=len(users), search=search, record_name='users')

        if len(users) > 10:
            offset_start = (page - 1) * 10
            offset_end = page * 10
            users = users[offset_start:offset_end]
    else:
        pagination = Pagination(css_framework='bootstrap3', page=page, total=users.count(), search=search, record_name='users')

        if users.count() > 10:
            if page == 1:
                offset = 0
            else:
                page -= 1
                offset = page * 10
            users = users.fetch(limit=10, offset=offset)

    return render_template('user/index.html', **locals())


@prefix.route('/inscrit', methods=['POST'])
def inscrit():

    exist_matricule = Users.query(
        Users.matricule == request.form['matricule']
    ).get()

    if exist_matricule:
        flash('Le matricule est utilise par une autre personne', 'danger')
    else:
        user = Users()
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.matricule = request.form['matricule']
        user.put()

        flash('Votre inscription a ete pris en compte', 'success')
    return redirect(url_for('home.home'))


@prefix.route('/login', methods=['POST'])
def login():
    matricule = request.form['matricule']
    user = Users.query(
        Users.matricule == matricule
    ).get()

    if not user:
        flash('Ce matricule n\'est pas incrit dans le jeu', 'danger')
        return redirect(url_for('home.home'))
    else:
        session['user_id'] = user.key.id()
        user.logged = True
        user.put()
        return redirect(url_for('user.participation'))


@prefix.route('/participation')
@login_required
def participation():

    participed = Parametre.query().get()

    question = Question.query().count()

    return render_template('user/participation.html', **locals())


@prefix.route('/participation/jeu', methods=['POST', 'GET'])
@login_required
def participation_jeu():

    import random

    list_questions = Question.query()
    all_numbre_question = 0
    questions = []
    for question in list_questions:
        if question.correct():
            all_numbre_question += 1
            questions.append(question)

    number_question = Parametre.query().get()
    number_question = number_question.nbr_question

    if all_numbre_question < number_question:
        number_question = all_numbre_question

    num_question = random.sample(range(0, all_numbre_question), number_question)

    if request.method == 'POST':

        participe = Participation()

        count = 0
        numbre_question = 0
        for reponse in request.form.getlist('reponse'):
            the_reponse = Reponse.get_by_id(int(reponse))
            if the_reponse.correct:
                count+=1
            numbre_question+=1



        participe.nbr_reponse = str(count)
        participe.pourcentage = float((count * 100) / numbre_question)
        participe.user = current_user.key
        participe.put()

        flash('Votre participation a ete enregistree. Merci et a la prochaine', 'success')
        return redirect(url_for('user.participation'))


    return render_template('user/participation_jeu.html', **locals())

