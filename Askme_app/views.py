from django.http import HttpResponseNotFound
from django.shortcuts import render
from . import models
from scripts.paginator import make_paginator

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
               'account': models.Accounts[0]}
    return render(request, 'settings.html', context=context)

def create_question(request):
    context = {'popular_tags': models.Popular_tags,
               'best_members': models.Best_members}
    return render(request, 'create_question.html', context=context)

def new_questions(request):
    questions = make_paginator(models.Questions, QUESTIONS_PER_PAGE, request)
    context = {'questions': questions,
               'popular_tags': models.Popular_tags,
               'best_members': models.Best_members}
    return render(request, 'new_questions.html', context=context)

def question(request, question_id):
    try:
        question_data = models.Questions[question_id]
    except:
        return HttpResponseNotFound("Question not found")

    answers = []
    for answer in models.Answers:
        if question_id == answer['question_id']:
            answers.append(answer)
    answers = make_paginator(answers, QUESTIONS_PER_PAGE, request)
    context = {'question': question_data,
               'answers': answers,
               'popular_tags': models.Popular_tags,
               'best_members': models.Best_members}
    return render(request, 'question.html', context=context)

def tag(request, tag_name):
    questions = []
    for cur_question in models.Questions:
        if tag_name in cur_question['tags']:
            questions.append(cur_question)
    questions = make_paginator(questions, QUESTIONS_PER_PAGE, request)
    context = {'questions': questions,
               'tag': tag_name,
               'popular_tags': models.Popular_tags,
               'best_members': models.Best_members}
    return render(request, 'tag.html', context=context)