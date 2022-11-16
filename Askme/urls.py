"""Askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Askme_app import views
# from views import index_view, registration_view, profile_view, auth_view, logout_view, create_question_view, \
#     question_view, profile_edit_view, vote_view, tag_view, user_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.new_questions, name='new_questions'),
    path('registration/', views.registration, name='registration'),
    path('auth/', views.auth, name='auth'),
    path('settings/', views.settings, name='settings'),
    path('create_question/', views.create_question, name='create_question'),
    path('questions/<int:question_id>/', views.question, name='question'),
    path('tags/<str:tag_name>/', views.tag, name='tag'),
]
