from django.conf.urls import patterns, url
from .views import QuestionAnswerResponseView, QuestionDeleteView, TrueFalseQuestionCreateView, \
	OpenEndedQuestionCreateView

urlpatterns = patterns('',
	url(r'^(?P<question>[-_\w]+)/responses/$', QuestionAnswerResponseView.as_view(), name='question-answer-reponse-detail'),
	url(r'^question/(?P<pk>[-_\d]+)/delete/$', QuestionDeleteView.as_view(), name='question-delete'),
    url(r'^question/boolean/create', TrueFalseQuestionCreateView.as_view(), name='boolean-question-create'),
    url(r'^question/open/create', OpenEndedQuestionCreateView.as_view(), name='open-question-create'),
)
