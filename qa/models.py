from django.db import models
from model_utils.models import TimeStampedModel


class AnswerOption(TimeStampedModel):
	text = models.TextField()


class Answer(TimeStampedModel):
	owner = models.ForeignKey('accounts.Instructor')
	answer_options = models.ManyToManyField('AnswerOption', related_name='option')
	correct_answer = models.ForeignKey('AnswerOption', related_name='correct')


class Question(TimeStampedModel):
	owner = models.ForeignKey('accounts.Instructor')
	lecture = models.ForeignKey('core.Lecture', blank=True, null=True, related_name='belongs_to')
	text = models.TextField()
	active = models.BooleanField(default=False)
	start_time = models.DateTimeField(blank=True, null=True)


class OpenEndedResponse(TimeStampedModel):
	owner = models.ForeignKey('accounts.Student')
	question = models.ForeignKey(Question)
	text = models.TextField()

	def has_feedback(self):
		return len(ResponseFeedback.objects.filter(response=self)) > 0


class ResponseFeedback(TimeStampedModel):
	owner = models.ForeignKey('accounts.Instructor')
	response = models.ForeignKey(OpenEndedResponse)
	feedback = models.TextField()


class ClosedEndedQuestion(Question):
	answer = models.ForeignKey('Answer')

	def activate(self):
		self.active = True

	def deactivate(self):
		self.active = False

	def get_response_count(self):
		return AnswerInstance.objects.filter(question=self).count()

	def get_answer(self):
		return self.answer


class AnswerInstance(TimeStampedModel):
	student = models.ForeignKey('accounts.Student')
	question = models.ForeignKey(Question)
	answer_option = models.ForeignKey(AnswerOption)

	def is_correct(self):
		return self.question.answer.correct_answer == self.answer_option


class LectureQuestion(TimeStampedModel):
	lecture = models.ForeignKey('core.Lecture')
	question = models.ForeignKey('Question')

