from django.contrib import admin
from .models import Answer, AnswerOption, Category, Question
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	pass

@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
	list_display = ('id', 'category', 'text')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
	list_display = ('id', 'created', 'owner', 'category', 'correct_answer')


def activate(modeladmin, request, queryset):
	for obj in queryset:
		obj.activate()


def deactivate(modeladmin,request, queryset):
	for obj in queryset:
		obj.deactivate()

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ('id', 'owner', 'text', 'answer', 'active')
	actions = [activate, deactivate]