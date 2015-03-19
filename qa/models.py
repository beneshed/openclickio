from django.db import models
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager

# Create your models here.
class Category(TimeStampedModel):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return u'%s' % self.name


class AnswerOption(TimeStampedModel):
	category = models.ForeignKey(Category)
	text = models.TextField()

	def __unicode__(self):
		return u'%s: %s' % (self.category, self.text)

class OwnedAnswerManager(models.Manager):
	def get_queryset(self, _professor):
		return super(OwnedAnswerManager, self).get_queryset().filter(owner=_professor)


class Answer(TimeStampedModel):
	owner = models.ForeignKey('accounts.Professor')
	category = models.ForeignKey('Category')
	answer_options = models.ManyToManyField('AnswerOption', related_name='option')
	correct_answer = models.ForeignKey('AnswerOption', related_name='correct')
	objects = models.Manager()
	owned = OwnedAnswerManager()

	def __unicode__(self):
		return u'%s: %s' % (self.category, self.correct_answer)


class ViewableQuestionManager(models.Manager):
	def get_queryset(self, _lecture):
		return super(ViewableQuestionManager, self).get_queryset().filter(active=True,owner=_lecture.professor)


class OwnedQuestionManager(models.Manager):
	def get_queryset(self, _user):
		return super(OwnedQuestionManager, self).get_querset().filter(owner=_user)


class Question(TimeStampedModel):
	owner = models.ForeignKey('accounts.Professor')
	text = models.TextField()
	answer = models.ForeignKey('Answer')
	active = models.BooleanField(default=False)
	objects = models.Manager()
	viewable = ViewableQuestionManager()
	owned = OwnedQuestionManager()
	tags = TaggableManager()

	def activate(self):
		self.active = True

	def deactivate(self):
		self.active = False


class LectureQuestion(TimeStampedModel):
	lecture = models.ForeignKey('core.Lecture')
	question = models.ForeignKey('Question')

