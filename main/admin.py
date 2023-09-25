from django.contrib import admin

# Register your models here.

from .models import StartEvent, AnswerEvent, ResultEvent


class StartEventAdmin(admin.ModelAdmin):
    readonly_fields = (
        "datetime",
        "id",
    )
    search_fields = (
        "referrer",
        "city",
        "datetime",
        "job",
        "device_type",
        "device_uid",
        "ip",
        "nickname",
    )
    list_display = (
        "referrer",
        "city",
        "datetime",
        "job",
        "device_type",
        "device_uid",
        "ip",
        "nickname",
    )
    list_filter = (
        "referrer",
        "city",
        "datetime",
        "job",
        "device_type",
        "device_uid",
        "ip",
        "nickname",
    )


class AnswerEventAdmin(admin.ModelAdmin):
    readonly_fields = (
        "datetime",
        "id",
    )
    search_fields = (
        "quiz_uid",
        "datetime",
        "job",
        "device_type",
        "device_uid",
        "ip",
        "nickname",
    )
    list_display = (
        "quiz_uid",
        "datetime",
        "job",
        "device_type",
        "device_uid",
        "ip",
        "nickname",
    )
    list_filter = (
        "quiz_uid",
        "datetime",
        "job",
        "device_type",
        "device_uid",
        "ip",
        "nickname",
    )


class ResultEventAdmin(admin.ModelAdmin):
    readonly_fields = ("datetime", "id", "marks")
    search_fields = (
        "datetime",
        "job",
        "device_type",
        "device_uid",
        "ip",
        "nickname",
        "marks",
    )
    list_display = (
        "datetime",
        "job",
        "device_type",
        "device_uid",
        "ip",
        "nickname",
        "marks",
    )
    list_filter = (
        "datetime",
        "job",
        "device_type",
        "device_uid",
        "ip",
        "nickname",
        "marks",
    )


admin.site.register(StartEvent, StartEventAdmin)
admin.site.register(AnswerEvent, AnswerEventAdmin)
admin.site.register(ResultEvent, ResultEventAdmin)
