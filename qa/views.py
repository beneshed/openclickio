from django.views.generic import TemplateView
from .models import Question, AnswerInstance, AnswerOption
from django.shortcuts import get_object_or_404
from braces.views import LoginRequiredMixin
from django.db.models import Count


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