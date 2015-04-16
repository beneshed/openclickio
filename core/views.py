from django.shortcuts import render
from django.views.generic import TemplateView, FormView, DetailView, View
from django.views.generic.list import ListView
from django.views.generic import CreateView
from .models import RegisteredLecture, Lecture
from qa.models import Question
from accounts.models import Instructor
from braces.views import LoginRequiredMixin
from .forms import RegisterLectureCodeForm, CreateLectureForm
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from registration.models import RegisteredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse

class StudentListLectureView(LoginRequiredMixin, ListView):
	template_name = 'list_lecture.html'
	model = RegisteredLecture

	def get_queryset(self):
		return RegisteredLecture.objects.filter(student__user=self.request.user)


class InstructorListLectureView(LoginRequiredMixin, ListView):
	template_name = 'list_lecture.html'
	model = Lecture

	def get_queryset(self):
		return Lecture.objects.filter(instructor=self.request.user.instructor)


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

	def form_valid(self, form):
		form.instance.instructor = self.request.user.instructor
		form.instance.university = self.request.user.instructor.university
		return super(CreateLectureView, self).form_valid(form)


class LectureDetailView(LoginRequiredMixin, DetailView):
	template_name = 'detail_lecture.html'
	model = Lecture

	def get_context_data(self, **kwargs):
		context = super(LectureDetailView, self).get_context_data(**kwargs)
		context['pending_students'] = RegisteredLecture.objects.filter(lecture=self.object, approved=False)
		context['registered_lectures'] = RegisteredLecture.objects.filter(lecture=self.object, approved=True)
		context['questions'] = Question.objects.filter(owner=self.request.user.instructor, lecture=self.object)
		return context


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
				context['classes'] = Lecture.objects.filter(instructor=self.request.user)
				context['is_instructor'] = True
			except ObjectDoesNotExist:
				pass
		return context


class UserRegisteredLectureApproveView(LoginRequiredMixin, View):

	def get(self, request, **kwargs):
		registration = get_object_or_404(RegisteredLecture,pk=self.kwargs['pk'])
		if self.kwargs['approved'] == 'true':
			registration.approve()
			registration.save()
		elif self.kwargs['approved'] == 'false':
			registration.deny()
			registration.save()
		else:
			return HttpResponse(status=400)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



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

