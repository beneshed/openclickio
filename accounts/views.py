from django.views.generic import CreateView, TemplateView, DetailView
from django.core.urlresolvers import reverse, reverse_lazy
from .models import Professor
from django.shortcuts import redirect
from core.models import University
from django.contrib.auth.models import User

class InstructorCreateView(TemplateView):
	template_name = "create_instructor.html"

	def get(self, request, *args, **kwargs):
		u = University.objects.get(pk=1)
		p = Professor.objects.create(user=request.user, university=u)
		p.save()
		return redirect('user-detail')


class UserDetailView(DetailView):
	template_name = "user_detail.html"
	model = User

	def get_context_data(self, **kwargs):
		context = super(UserDetailView, self).get_context_data(**kwargs)
		context['student'] = None
		context['professor'] = None
		if self.request.user.student is not None and self.request.user.professor is None:
			context['student'] = self.request.user.student
		elif self.request.user.student is None and self.request.user.professor is not None:
			context['professor'] = self.request.user.professor
		return context

