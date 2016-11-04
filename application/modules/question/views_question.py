__author__ = 'Ronald'

from ...modules import *
from models_question import Question, Reponse


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)
prefix = Blueprint('question', __name__)


@prefix.route('')
def index():
    menu = 'question'

    search = False
    q = request.args.get('q')
    if q:
        search = True
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    list_question = Question.query()
    pagination = Pagination(css_framework='bootstrap3', page=page, total=list_question.count(), search=search, record_name='users')

    if list_question.count() > 10:
        if page == 1:
            offset = 0
        else:
            page -= 1
            offset = page * 10
        users = list_question.fetch(limit=10, offset=offset)

    return render_template('question/index.html', **locals())


@prefix.route('/create', methods=['POST', 'GET'])
@prefix.route('/create/<int:id_question>', methods=['POST', 'GET'])
def create_question(id_question=None):
    menu = 'question'

    if id_question:
        the_question = Question.get_by_id(id_question)
    else:
        the_question = Question()

    if request.method == 'POST':
        question = request.form['question']

        the_question.libelle = question

        total_question = Question.query().count()
        the_question.num = total_question

        quest = the_question.put()

        return redirect(url_for('question.views_question', id_question=quest.id()))

    return render_template('question/create.html', **locals())


@prefix.route('/create/reponse/<int:id_question>', methods=['POST', 'GET'])
@prefix.route('/create/reponse/<int:id_question>/<int:id_reponse>', methods=['POST', 'GET'])
def create_reponse(id_question, id_reponse=None):
    menu = 'question'

    if id_reponse:
        the_reponse = Reponse.get_by_id(id_reponse)
    else:
        the_reponse = Reponse()

    the_question = Question.get_by_id(id_question)

    if request.method == 'POST':
        reponse = request.form['question']


        the_reponse.libelle = reponse
        the_reponse.question = the_question.key
        the_reponse.put()

        return redirect(url_for('question.views_question', id_question=the_question.key.id()))

    return render_template('question/create_reponse.html', **locals())


@prefix.route('/views/<int:id_question>')
def views_question(id_question):
    menu = 'question'

    the_question = Question.get_by_id(id_question)

    return render_template('question/views.html', **locals())


@prefix.route('/reponse/correct/<int:id_reponse>')
def correct_reponse(id_reponse):

    reponse = Reponse.get_by_id(id_reponse)

    for reponses in reponse.question.get().list_reponse():
        if reponses.correct:
            reponses.correct = False
            reponses.put()

    id_question = reponse.question.get().key.id()

    if reponse.correct:
        reponse.correct = False
    else:
        reponse.correct = True
    reponse.put()

    return redirect(url_for('question.views_question', id_question=id_question))


@prefix.route('/reponse/delete/<int:id_reponse>')
def delete_reponse(id_reponse):
    reponse = Reponse.get_by_id(id_reponse)

    id_question = reponse.question.get().key.id()

    reponse.key.delete()

    return redirect(url_for('question.views_question', id_question=id_question))


@prefix.route('/delete/<int:id_question>')
def delete_question(id_question):
    question = Question.get_by_id(id_question)

    for reponse in question.list_reponse():
        reponse.key.delete()


    all_question = Question.query()
    num = 1
    for question in all_question:
        question.num = num
        question.put()
        num += 1


    question.key.delete()

    return redirect(url_for('question.index'))
