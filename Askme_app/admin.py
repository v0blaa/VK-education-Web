from django.contrib import admin

from Askme_app.models import Question, Answer, Notification, Tag, Profile, Vote

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Notification)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Vote)
