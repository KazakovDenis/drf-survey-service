from django.contrib import admin

from .models import Survey, SurveyQuestion


class SurveyQuestionInline(admin.TabularInline):
    model = SurveyQuestion
    extra = 0


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_from', 'date_to')
    list_filter = ('name', 'date_from', 'date_to')
    search_fields = ('name', 'description')
    fields = ('name', 'description', 'date_to')

    inlines = [
        SurveyQuestionInline,
    ]
