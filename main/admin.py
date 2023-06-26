from django.contrib import admin

# Register your models here.

from .models import StartEvent, AnswerEvent, ResultEvent


class StartEventAdmin(admin.ModelAdmin):
    readonly_fields = ("datetime",)


class AnswerEventAdmin(admin.ModelAdmin):
    readonly_fields = ("datetime",)


class ResultEventAdmin(admin.ModelAdmin):
    readonly_fields = ("datetime",)


admin.site.register(StartEvent, StartEventAdmin)
admin.site.register(AnswerEvent, AnswerEventAdmin)
admin.site.register(ResultEvent, ResultEventAdmin)
