from Askme_app.models import Question, Notification, Answer, Tag, Profile, Vote

def questions_for_tag(tag_name):
    return Question.objects.filter(tags__text=tag_name).order_by('-created')

def new_questions():
    sort_key = '-created'
    return Question.objects.order_by(sort_key)

def hot_questions(request):
    if request.GET.get('popular') is not None:
        sort_key = '-total_votes'
    elif request.GET.get('answered') is not None:
        sort_key = '-total_answers'
    else:
        sort_key = '-created'

    return Question.objects.order_by(sort_key)

def answers_for_question(question_id):
    return Answer.objects.filter(question=question_id)


def tags_for_question(question):
    return question.tags.all()

def get_question_with_id(question_id):

    return Question.objects.get(id=question_id)