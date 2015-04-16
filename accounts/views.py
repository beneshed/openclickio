from django.views.generic import CreateView, TemplateView, DetailView

from .models import Instructor
from django.shortcuts import redirect
from core.models import University
from django.contrib.auth.models import User

class InstructorCreateView(TemplateView):
	template_name = "create_instructor.html"

	def get(self, request, *args, **kwargs):
		u = University.objects.get(pk=1)
		p = Instructor.objects.create(user=request.user, university=u)
		p.save()
		return redirect('user-detail')


class UserDetailView(DetailView):
	template_name = "user_detail.html"
	model = User

	def get_context_data(self, **kwargs):
		context = super(UserDetailView, self).get_context_data(**kwargs)
		context['student'] = None
		context['is_student'] = False
		context['is_instructor'] = False
		context['instructor'] = None
		if self.request.user.student is not None and self.request.user.instructor is None:
			context['student'] = self.request.user.student
			context['is_student'] = True
		elif self.request.user.student is None and self.request.user.instructor is not None:
			context['instructor'] = self.request.user.instructor
			context['is_instructor'] = True
		return context


class PublicProfileView(DetailView):
	template_name = "user_detail.html"
	model = User

	def get_context_data(self, **kwargs):
		context = super(PublicProfileView, self).get_context_data(**kwargs)
		context['student'] = None
		context['is_student'] = False
		context['is_instructor'] = False
		context['instructor'] = None
		if self.request.user.student is not None and self.request.user.instructor is None:
			context['student'] = self.request.user.student
			context['is_student'] = True
		elif self.request.user.student is None and self.request.user.instructor is not None:
			context['instructor'] = self.request.user.instructor
			context['is_instructor'] = True
		return context