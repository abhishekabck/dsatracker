from django.contrib import admin
from .models import DSATopics, DSAPatternQuestions, DSAPattern
# Register your models here.

# This representation helps in customizing the admin panel of the model

@admin.register(DSAPatternQuestions)
class DSAPatternQuestionsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question_heading",
        "question_URL",
        'solved',
    )

    search_fields = (
        'id',
        'question_heading',
        'pattern__pattern_name',
        'pattern__topic__topic_name',
    )

    actions = ['mark_solved', 'mark_unsolved']
    def mark_solved(self, request, queryset):
        queryset.update(solved=True)
    def mark_unsolved(self, request, queryset):
        queryset.update(solved=False)

    mark_unsolved.short_description = "Mark selected questions as unsolved"
    mark_solved.short_description = "Mark selected questions as solved"

    list_filter = ('solved',)
    readonly_fields = ('id', 'question_URL')
    exclude = ('solved', 'solved_date')

class DSAPatternQuestionInline(admin.TabularInline):
    model = DSAPatternQuestions
    extra = 1

@admin.register(DSAPattern)
class DSAPatternAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'topic__topic_name',
        'pattern_name',
    )
    readonly_fields = ('id',)

    search_fields = ('pattern_name', 'topic__topic_name')
    inlines = [DSAPatternQuestionInline]


class DSAPatternInline(admin.StackedInline):
    model = DSAPattern
    extra = 1

@admin.register(DSATopics)
class DSATopicsAdmin(admin.ModelAdmin):
    list_display = ('topic_name',)

    search_fields = ('topic_name',)
    readonly_fields = ('id',)
    inlines = [DSAPatternInline]

# admin.site.register(DSATopics)
# admin.site.register(DSAPatternQuestions) # This part here simply adds that particular model to the admin panel
# admin.site.register(DSAPattern)