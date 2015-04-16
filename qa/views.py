from django.views.generic import TemplateView, DeleteView, FormView
from .models import Question, AnswerInstance, AnswerOption,\
	ClosedEndedQuestion, Answer
from core.models import Lecture
from django.shortcuts import get_object_or_404
from braces.views import LoginRequiredMixin
from django.db.models import Count
from .forms import GenericQuestionForm, BooleanQuestionForm, OpenQuestionForm
from django.core.urlresolvers import reverse, reverse_lazy

class QuestionAnswerResponseView(LoginRequiredMixin, TemplateView):
	template_name = 'question_answer_response.html'

	def get_context_data(self, **kwargs):
		context = super(QuestionAnswerResponseView, self).get_context_data(**kwargs)
		question = get_object_or_404(Question, id=self.kwargs['question'])
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