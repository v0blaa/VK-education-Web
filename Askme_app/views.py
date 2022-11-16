from django.http import HttpResponseNotFound
from django.shortcuts import render
from . import models
from scripts.paginator import make_paginator
from Askme_app.queries import queries

QUESTIONS_PER_PAGE = 4

def registration(request):
    context = {'popular_tags': models.Popular_tags,
               'best_members': models.Best_members}
    return render(request, 'registration.html', context=context)

def auth(request):
    context = {'popular_tags': models.Popular_tags,
               'best_members': models.Best_members}
    return render(request, 'auth.html', context=context)

def settings(request):
    context = {'popular_tags': models.Popular_tags,
               'best_members': models.Best_members,
               'account': models.Profile.objects[0]}
    return render(request, 'settings.html', context=context)

def create_question(request):
    context = {'popular_tags': models.Popular_tags,
               'best_members': models.Best_members}
    return render(request, 'create_question.html', context=context)

def new_questions(request):
    questions = queries.new_questions()
    questions = make_paginator(questions, QUESTIONS_PER_PAGE, request)
    context = {'questions': questions,
               'popular_tags': models.Popular_tags,
               'best_members': models.Best_members}
    return render(request, 'new_questions.html', context=context)


def hot_questions(request):
    questions = queries.hot_questions(request)

    questions = make_paginator(questions, QUESTIONS_PER_PAGE, request)
    context = {'questions': questions,
               'popular_tags': models.Popular_tags,
               'best_members': models.Best_members}
    return render(request, 'new_questions.html', context=context)

def question(request, question_id):
    try:
        question = queries.get_question_with_id(question_id)
    except:
        return HttpResponseNotFound("Question not found")

    answers = queries.answers_for_question(question_id)
    answers = make_paginator(answers, QUESTIONS_PER_PAGE, request)
    context = {'question': question,
               'answers': answers,
               'popular_tags': models.Popular_tags,
               'best_members': models.Best_members}
    return render(request, 'question.html', context=context)

def tag(request, tag_name):
    questions = queries.questions_for_tag(tag_name)
    questions = make_paginator(questions, QUESTIONS_PER_PAGE, request)
    context = {'questions': questions,
               'tag': tag_name,
               'popular_tags': models.Popular_tags,
               'best_members': models.Best_members}
    return render(request, 'tag.html', context=context)