from django.shortcuts import render
from django.views.generic import TemplateView, FormView, DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView
from .models import RegisteredLecture, Lecture
from accounts.models import Professor
from braces.views import LoginRequiredMixin
from .forms import RegisterLectureCodeForm, CreateLectureForm
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy

class StudentListLectureView(LoginRequiredMixin, ListView):
	template_name = 'list_lecture.html'
	model = RegisteredLecture

	def get_queryset(self):
		return RegisteredLecture.objects.filter(student__user=self.request.user)


class InstructorListLectureView(LoginRequiredMixin, ListView):
	template_name = 'list_lecture.html'
	model = Lecture

	def get_queryset(self):
		return self.request.user.professor.lectures


class RegisteredLectureCreateView(LoginRequiredMixin, FormView):
	template_name = 'register_lecture.html'
	form_class = RegisterLectureCodeForm
	success_url = reverse_lazy('student-class-list')

	def form_valid(self, form):
		lecture = get_object_or_404(Lecture, registration_code=form.data['code'])
		register = RegisteredLecture.objects.create(lecture=lecture, student=self.request.user.student)
		register.save()


class CreateLectureView(LoginRequiredMixin, CreateView):
	template_name = 'create_lecture.html'
	model = Lecture
	form_class = CreateLectureForm
	success_url = reverse_lazy('instructor-class-list')


class LectureDetailView(LoginRequiredMixin, DetailView):
	template_name = 'detail_lecture.html'
	model = Lecture


