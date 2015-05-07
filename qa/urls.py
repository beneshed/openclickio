from django.conf.urls import patterns, url
from .views import QuestionAnswerResponseView, QuestionDeleteView, TrueFalseQuestionCreateView, \
	OpenEndedQuestionCreateView, MultipleChoicePartOne, MultipleChoicePartTwo, QuestionActivateView, QuestionResponseView

urlpatterns = patterns('',
	url(r'^(?P<question>[-_\w]+)/responses/$', QuestionAnswerResponseView.as_view(), name='question-answer-reponse-detail'),
	url(r'^question/(?P<pk>[-_\d]+)/delete/$', QuestionDeleteView.as_view(), name='question-delete'),
	url(r'^question/(?P<pk>[-_\d]+)/activate/$', QuestionActivateView.as_view(), name='question-activate'),
	url(r'^question/(?P<pk>[-_\d]+)/response/$', QuestionResponseView.as_view(), name='question-response'),
    url(r'^question/boolean/create', TrueFalseQuestionCreateView.as_view(), name='boolean-question-create'),
    url(r'^question/open/create', OpenEndedQuestionCreateView.as_view(), name='open-question-create'),
    url(r'^question/multiple/step/', MultipleChoicePartOne.as_view(), name='multiple-choice-one'),
    url(r'^question/multiple/(?P<number>[-_\d]+)/', MultipleChoicePartTwo.as_view(), name='multiple-choice'),
)
