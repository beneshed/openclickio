from django.contrib import admin
from .models import University, Lecture, RegisteredLecture
from qa.models import LectureQuestion
# Register your models here.
# Register your models here.
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
	list_display = ('id', 'created', 'name', 'email_suffix')

class RosterInline(admin.TabularInline):
	model = RegisteredLecture

class QuestionInline(admin.TabularInline):
	model = LectureQuestion

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
	list_display = ('id', 'created', 'professor', 'university', 'department', 'name')
	inlines = (RosterInline, QuestionInline, )

	def professor(self, obj):
		if len(obj.professors_lectures.all()) > 0:
			return obj.professors_lectures.all()[0]
		else:
			return None

