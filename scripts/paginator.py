from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404


def make_paginator(objects, max_objects_per_page, request):
    paginator = Paginator(objects, max_objects_per_page)
    page_num = request.GET.get('page')
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page