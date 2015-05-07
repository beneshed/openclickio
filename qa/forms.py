from django import forms
from core.models import Lecture
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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


class MultipleChoiceNumberChoice(forms.Form):
	number = forms.IntegerField(min_value=2, max_value=5)

	def __init__(self, *args, **kwargs):
		super(MultipleChoiceNumberChoice, self).__init__(*args,**kwargs)
		self.helper = FormHelper(self)
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Submit'))