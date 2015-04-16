from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import QuestionAnswerResponseView

urlpatterns = patterns('',
	url(r'^(?P<question>[-_\w]+)/responses/$', QuestionAnswerResponseView.as_view(), name='question-answer-reponse-detail'),
)
