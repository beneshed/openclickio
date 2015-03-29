from django.shortcuts import render
from django.views.generic import TemplateView, FormView, DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView
from .models import RegisteredLecture, Lecture
from accounts.models import Professor
from braces.views import LoginRequiredMixin
from .forms import RegisterLectureCodeForm, CreateLectureForm
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from registration.models import RegisteredMixin
from django.core.exceptions import ObjectDoesNotExist


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


class LectureListView(LoginRequiredMixin, ListView):
	template_name = 'list_lecture.html'
	model = Lecture


class UserRegisteredLectureView(LoginRequiredMixin, TemplateView):
	template_name = 'list_lecture.html'

	def get_context_data(self, **kwargs):
		context = super(UserRegisteredLectureView, self).get_context_data(**kwargs)
		context['classes'] = None
		context['is_student'] = False
		context['is_instructor'] = False
		try:
			context['classes'] = self.request.user.student.classes.all()
			print self.request.user.student.classes.all()
			context['is_student'] = True
		except ObjectDoesNotExist:
			try:
				context['classes'] = self.request.user.professor.classes.all()
				context['is_instructor'] = True
			except ObjectDoesNotExist:
				pass
		return context

class HomePageView(TemplateView):
	template_name = 'index.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated() and request.user.is_active:
			return redirect('dashboard')
		else:
			context = self.get_context_data(**kwargs)
			return self.render_to_response(context)

	def get_context_data(self, **kwargs):
		context = super(HomePageView, self).get_context_data(**kwargs)
		context['is_registered'] = self.request.user.is_active
		return context


class DashboardView(TemplateView):
	template_name = 'dashboard.html'

