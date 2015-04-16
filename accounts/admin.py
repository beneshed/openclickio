from django.contrib import admin

# Register your models here.
from .models import Student, Instructor

class InstructorInline(admin.StackedInline):
	model = Instructor
	can_delete = False
	verbose_name_plural = 'Professors'

class StudentInline(admin.StackedInline):
	model = Student
	can_delete = False
	verbose_name_plural = 'Students'


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
	def has_delete_permission(self, request, obj=None): # note the obj=None
		return False

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	def has_delete_permission(self, request, obj=None):
		return False
