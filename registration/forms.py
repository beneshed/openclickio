from django import forms
from accounts.models import Student, Professor
class StudentRegistrationForm(forms.ModelForm):
	class Meta:
		model = Student

class ProfessorRegistrationForm(forms.ModelForm):
	class Meta:
		model = Professor