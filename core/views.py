from django.shortcuts import render
from django.views.generic import TemplateView, FormView, DetailView, View, DeleteView
from django.views.generic.list import ListView
from django.views.generic import CreateView
from .models import RegisteredLecture, Lecture, AttendanceRecord
from qa.models import Question, ClosedEndedQuestion
from braces.views import LoginRequiredMixin
from .forms import RegisterLectureCodeForm, CreateLectureForm
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse

class StudentListLectureView(LoginRequiredMixin, ListView):
	template_name = 'student_list_lecture.html'
	model = RegisteredLecture

	def get_queryset(self):
		return RegisteredLecture.objects.filter(student=self.request.user.student)


class InstructorListLectureView(LoginRequiredMixin, ListView):
	template_name = 'instructor_list_lecture.html'
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
		context['in_class_students'] = AttendanceRecord.objects.filter(lecture=self.object)
		context['registered_lectures'] = RegisteredLecture.objects.filter(lecture=self.object, approved=True)
		context['questions'] = Question.objects.filter(owner=self.request.user.instructor, lecture=self.object, closedendedquestion=None)
		context['closed_questions'] = ClosedEndedQuestion.objects.filter(owner=self.request.user.instructor, lecture=self.object)
		return context


class StudentLectureDetailView(LoginRequiredMixin, DetailView):
	template_name = 'student_lecture_detail.html'
	model = Lecture

	def get_context_data(self, **kwargs):
		context = super(StudentLectureDetailView, self).get_context_data(**kwargs)
		context['questions'] = Question.objects.filter(owner=self.object.instructor, lecture=self.object, closedendedquestion=None, active=True)
		context['closed_questions'] = ClosedEndedQuestion.objects.filter(owner=self.object.instructor, lecture=self.object, active=True)
		return context


class LectureListView(LoginRequiredMixin, ListView):
	template_name = 'list_lecture.html'
	model = Lecture


class CreateAttendanceView(LoginRequiredMixin, View):

	def get(self, request, **kwargs):
		lecture = get_object_or_404(Lecture, pk=self.kwargs['pk'])
		registrations = RegisteredLecture.objects.filter(lecture=lecture)
		for registration in registrations:
			AttendanceRecord.objects.create(lecture=lecture, student=registration.student)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class RosterDetailView(LoginRequiredMixin, TemplateView):
	template_name = 'roster.html'

	def get_context_data(self, **kwargs):
		context = super(RosterDetailView, self).get_context_data(**kwargs)
		lecture = Lecture.objects.get(pk=self.kwargs['pk'])
		context['roster'] = lecture.roster.all
		context['back_url'] = reverse_lazy('detail-lecture', kwargs={'pk':lecture.id})
		return context


class RegistrationDeleteView(LoginRequiredMixin, DeleteView):
	model = RegisteredLecture

	def get_success_url(self):
		return self.request.META.get('HTTP_REFERER')


class UserRegisteredLectureView(LoginRequiredMixin, TemplateView):
	template_name = 'student_list_lecture.html'

	def get_template_names(self):
		try:
			if self.request.user.instructor is not None:
				return 'instructor_list_leture.html'
		except ObjectDoesNotExist:
			try:
				if self.request.user.student is not None:
					return 'student_list_lecture.html'
			except ObjectDoesNotExist:
				pass

	def get_context_data(self, **kwargs):
		context = super(UserRegisteredLectureView, self).get_context_data(**kwargs)
		try:
			if self.request.user.instructor is not None:
				context['object_list'] = Lecture.objects.filter(instructor=self.request.user)
		except ObjectDoesNotExist:
			try:
				if self.request.user.student is not None:
					context['object_list'] = RegisteredLecture.objects.filter(student=self.request.user.student)
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

