from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager


class Instructor(TimeStampedModel):
	user = models.OneToOneField(User)
	university = models.ForeignKey('core.University')

	def __unicode__(self):
		return u'%s: %s' % (self.user.get_full_name(), self.university)

	class Meta:
		verbose_name_plural = 'Professors'
		permissions = (
		('ask_question', 'Ask Question'),
		)


class Student(TimeStampedModel):
	user = models.OneToOneField(User)
	university = models.ForeignKey('core.University')
	classes = models.ManyToManyField('core.Lecture')
	#stats = models.OneToOneField('stats.Stat')

	def __unicode__(self):
		return u'%s: %s' % (self.user.get_full_name(), self.university)

	class Meta:
		permissions = (
			('view_question', 'View Question'),
			('answer_question', 'Answer Question'),
			('check_grade', 'Check Grade'),
		)