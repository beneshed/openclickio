from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from .models import Registration
from accounts.models import Student, Professor
from core.models import University
from django.shortcuts import redirect

# Create your views here.
class ActivationView(TemplateView):
	template_name = "activation.html"

	def get(self, request, *args, **kwargs):
		activation_key = self.kwargs['activation_key']
		registration = get_object_or_404(Registration, activation_key=activation_key)
		registration.verified = True
		registration.save()
		user = registration.user
		user.is_active = True
		user.save()
		return super(ActivationView, self).get(request, *args, **kwargs)


class StudentRegistrationView(TemplateView):
	template_name = "student_registration.html"

	def get(self, request, *args, **kwargs):
		uni = University.objects.get(pk=1)
		Student.objects.get_or_create(university=uni ,user=self.request.user)
		return redirect('student-class-list')


class InstructorRegistrationView(FormView):
	template_name = "professor_registration.html"

	def get(self, request, *args, **kwargs):
		uni = University.objects.get(pk=1)
		Professor.objects.get_or_create(university=uni, user=self.request.user)
		return redirect('instructor-class-list')



