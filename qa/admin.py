from django.contrib import admin
from .models import Answer, AnswerOption, AnswerInstance, Question,\
	OpenEndedResponse, ClosedEndedQuestion
# Register your models here.

@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
	list_display = ('id', 'text')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
	list_display = ('id', 'created', 'owner', 'correct_answer')

@admin.register(AnswerInstance)
class AnswerInstanceAdmin(admin.ModelAdmin):
	list_display = ('id', 'created', 'student', 'question', 'answer_option')


def activate(modeladmin, request, queryset):
	for obj in queryset:
		obj.activate()


def deactivate(modeladmin,request, queryset):
	for obj in queryset:
		obj.deactivate()


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ('id', 'owner', 'text', 'active')
	actions = [activate, deactivate]

@admin.register(ClosedEndedQuestion)
class ClosedEndedQuestionAdmin(admin.ModelAdmin):
	list_display = ('id', 'owner', 'text', 'answer', 'active')
	actions = [activate, deactivate]