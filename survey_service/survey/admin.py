from django.contrib import admin

from .models import Scheme, SchemeQuestion


class SurveyQuestionInline(admin.TabularInline):
    model = SchemeQuestion
    extra = 0


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_from', 'date_to')
    list_filter = ('name', 'date_from', 'date_to')
    search_fields = ('name', 'description')
    fields = ('name', 'description', 'date_to')

    inlines = [
        SurveyQuestionInline,
    ]
