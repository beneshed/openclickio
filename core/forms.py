from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Lecture

class RegisterLectureCodeForm(forms.Form):
	code = forms.CharField(help_text="Input registration code given by professor")

	def __init__(self, *args, **kwargs):
		super(RegisterLectureCodeForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Submit'))


class CreateLectureForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(CreateLectureForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Submit'))


	class Meta:
		model = Lecture
		exclude = ['university', 'instructor', 'roster', 'questions']
