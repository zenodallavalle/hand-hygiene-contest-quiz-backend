from django.contrib import admin

# Register your models here.

from .models import StartEvent, AnswerEvent, ResultEvent

admin.site.register(StartEvent)
admin.site.register(AnswerEvent)
admin.site.register(ResultEvent)
