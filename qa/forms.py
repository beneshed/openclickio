from django import forms
from core.models import Lecture


class GenericQuestionForm(forms.Form):
	text = forms.CharField(label='Question')
	is_correct = forms.BooleanField(help_text='Is this the correct answer?')


class OpenQuestionForm(forms.Form):
	text = forms.CharField(label="Question")
	lecture = forms.ModelChoiceField(queryset=Lecture.objects.all())

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('userid', None)
		super(OpenQuestionForm, self).__init__(*args, **kwargs)

		if user:
			self.fields['lecture'].queryset = Lecture.objects.filter(instructor=user.instructor)

	def is_valid(self):
		return True


class BooleanQuestionForm(forms.Form):
	text = forms.CharField(label='Question')
	is_true = forms.BooleanField()
	lecture = forms.ModelChoiceField(queryset=Lecture.objects.all())

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('userid', None)
		super(BooleanQuestionForm, self).__init__(*args, **kwargs)

		if user:
			self.fields['lecture'].queryset = Lecture.objects.filter(instructor=user.instructor)

	def is_valid(self):
		return True