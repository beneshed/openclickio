from django.views.generic import TemplateView, DeleteView, FormView, View
from django.shortcuts import render
from .models import Question, AnswerInstance, AnswerOption,\
	ClosedEndedQuestion, Answer
from core.models import Lecture
from django.shortcuts import get_object_or_404
from braces.views import LoginRequiredMixin
from django.db.models import Count
from .forms import GenericQuestionForm, BooleanQuestionForm, OpenQuestionForm, MultipleChoiceNumberChoice
from django.core.urlresolvers import reverse, reverse_lazy
from django import forms
from django.template.response import SimpleTemplateResponse
from django.http import HttpResponseRedirect, HttpResponseServerError
import re

class QuestionAnswerResponseView(LoginRequiredMixin, TemplateView):
	template_name = 'question_answer_response.html'

	def get_context_data(self, **kwargs):
		context = super(QuestionAnswerResponseView, self).get_context_data(**kwargs)
		question = get_object_or_404(ClosedEndedQuestion, id=self.kwargs['question'])
		context['question'] = question
		context['responses'] = AnswerInstance.objects.filter(question=question)
		dictionary_response = AnswerInstance.objects.filter(question=question)\
			.values('answer_option')\
			.annotate(response_count=Count('answer_option'))
		responses = []
		for dict in dictionary_response:
			answer_option = AnswerOption.objects.get(pk=dict['answer_option'])
			responses.append((answer_option.text, dict['response_count']))
		print responses
		context['response_stats'] = responses
		return context


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
	model = Question

	def get_success_url(self):
		return self.request.META.get('HTTP_REFERER')


class TrueFalseQuestionCreateView(LoginRequiredMixin, FormView):
	form_class = BooleanQuestionForm
	template_name = 'generic_form.html'

	def get_form_kwargs(self):
		return {'userid': self.request.user}

	def form_valid(self, form):
		#create true/false
		true = AnswerOption.objects.create(text='True')
		false = AnswerOption.objects.create(text='False')
		options = (true, false)
		lecture = Lecture.objects.get(pk=self.request.POST['lecture'])
		answer = None
		if self.request.POST['is_true'] == 'on':
			answer = Answer.objects.create(owner=self.request.user.instructor, correct_answer=true)
			answer.answer_options = options
			answer.save()
		elif self.request.POST['is_true'] == 'off':
			answer = Answer.objects.create(owner=self.request.user.instructor, correct_answer=false)
			answer.answer_options = options
			answer.save()
		ClosedEndedQuestion.objects.create(owner=self.request.user.instructor, answer=answer, text=self.request.POST['text'], lecture=lecture)
		return super(TrueFalseQuestionCreateView, self).form_valid(form)

	def get_success_url(self):
		lecture = self.request.POST['lecture']
		return reverse_lazy('detail-lecture', kwargs={'pk': lecture})


class OpenEndedQuestionCreateView(LoginRequiredMixin, FormView):
	form_class = OpenQuestionForm
	template_name = 'generic_form.html'

	def get_form_kwargs(self):
		return {'userid': self.request.user}

	def form_valid(self, form):
		lecture = Lecture.objects.get(pk=self.request.POST['lecture'])
		Question.objects.create(owner=self.request.user.instructor, text=self.request.POST['text'], lecture=lecture)
		return super(OpenEndedQuestionCreateView, self).form_valid(form)

	def get_success_url(self):
		lecture = self.request.POST['lecture']
		return reverse_lazy('detail-lecture', kwargs={'pk': lecture})



class MultipleChoicePartTwo(LoginRequiredMixin, View):

	def get(self, request, **kwargs):
		number = self.kwargs['number']
		form = forms.Form()
		form.fields['question'] = forms.CharField(label='Question Text?')
		form.fields['lecture'] = forms.ModelChoiceField(queryset=Lecture.objects.filter(instructor=self.request.user.instructor))
		for i in range(1, int(number) + 1):
			form.fields['choice_%s' % i] = forms.CharField(label='Option ' + str(i))
			form.fields['answer_%s' % i] = forms.BooleanField(label='Is Answer')
		return render(request, 'multiple_choice.html', {'form': form})

	def post(self, request, **kwargs):
		lecture = Lecture.objects.get(pk=request.POST['lecture'])
		options = {}
		answer_options = []
		for value in self.request.POST:
			number = value[-1]
			my_type = value[:-2]
			if my_type == 'choice':
				answer_option = AnswerOption.objects.create(text=request.POST[value])
				answer_options.append(answer_option)
				options[number] = answer_option
			elif my_type == 'answer':
				the_answer = Answer.objects.create(owner=request.user.instructor, correct_answer=options[number])
				the_answer.answer_options = answer_options
				the_answer.save()
				my_question = ClosedEndedQuestion.objects.create(text=request.POST['question'], owner=request.user.instructor, lecture=lecture, answer=the_answer)
		return HttpResponseRedirect(reverse_lazy('detail-lecture', kwargs={'pk': request.POST['lecture']}))


class MultipleChoicePartOne(LoginRequiredMixin, FormView):
	template_name = 'multiple_choice_one.html'
	form_class = MultipleChoiceNumberChoice

	def get_success_url(self):
		return reverse('multiple-choice', kwargs={'number': self.request.POST['number']})


class QuestionActivateView(LoginRequiredMixin, View):

	def get(self, request, **kwargs):
		try:
			question = ClosedEndedQuestion.objects.get(pk=self.kwargs['pk'])
			question.activate()
			question.save()
		except ClosedEndedQuestion.DoesNotExist:
			pass
		try:
			question = Question.objects.get(pk=self.kwargs['pk'])
			question.activate()
			question.save()
		except Question.DoesNotExist:
			pass
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class QuestionResponseView(LoginRequiredMixin, View):

	def get(self, request, **kwargs):
		form = forms.Form()
		try:
			question = ClosedEndedQuestion.objects.get(pk=self.kwargs['pk'])
			answers = question.answer.answer_options
			for i, answer in enumerate(answers.all()):
				print answer
				form.fields['option_%s' % answer.pk] = forms.BooleanField(label=str(answer.text))
			return render(request, 'question_response.html', {'form': form})
		except ClosedEndedQuestion.DoesNotExist:
			try:
				question = Question.objects.get(pk=self.kwargs['pk'])
				answers = AnswerOption.objects.filter(question=question)
				if answers.exists():
					form = forms.Form()
					for i, answer in enumerate(answers):
						form.fields['option_%s' % i] = forms.BooleanField(label=str(answer.text))
					return render(request, 'question_response.html', {'form': form})
			except Question.DoesNotExist:
				pass
		return HttpResponseServerError()

	def post(self, request, **kwargs):
		try:
			question = ClosedEndedQuestion.objects.get(pk=self.kwargs['pk'])
			for value in self.request.POST:
				if value[0:6] == 'option':
					pk = re.findall(r'\d+', str(value))
					option = AnswerOption.objects.get(pk=pk[0])
					AnswerInstance.objects.create(student=request.user.student, question=question, answer_option=option)
					return HttpResponseRedirect(reverse_lazy('student-detail-lecture', kwargs={'pk': question.lecture.pk}))
		except ClosedEndedQuestion.DoesNotExist:
			pass