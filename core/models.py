from django.db import models
from model_utils.models import TimeStampedModel
from datetime import date
from randomslugfield import RandomSlugField
from accounts.models import Professor


class University(TimeStampedModel):
	name = models.CharField(max_length=100)
	email_suffix = models.CharField(max_length=25)

	def __unicode__(self):
		return u'%s' % self.name

	class Meta:
		verbose_name_plural = 'Universities'


class RegisteredLecture(TimeStampedModel):
	lecture = models.ForeignKey('Lecture')
	student = models.ForeignKey('accounts.Student')
	approved = models.BooleanField(default=False)


class Lecture(TimeStampedModel):
	university = models.ForeignKey(University)
	department = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	year = models.PositiveSmallIntegerField(default=date.today().year)
	code = models.PositiveIntegerField(default=0)
	registration_code = RandomSlugField(length=7)
	roster = models.ManyToManyField('accounts.Student', through='RegisteredLecture', blank=True)
	questions = models.ManyToManyField('qa.Question', through='qa.LectureQuestion', blank=True)

	def __unicode__(self):
		return u'%s:%s %d' % (self.department, self.name, self.year)

	def professor(self):
		for professor in Professor.objects.all():
			if self in professor.lectures.all():
				return professor
		return None

	def enrollment_count(self):
		return len(self.roster.all())

	class Meta:
		verbose_name = 'Class'
		verbose_name_plural = 'Classes'
		unique_together = ('university', 'department', 'name', 'year', 'code')




