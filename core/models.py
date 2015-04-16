from django.db import models
from model_utils.models import TimeStampedModel
from datetime import date
from randomslugfield import RandomSlugField
from accounts.models import Instructor


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

	def approve(self):
		self.approved = True

	def deny(self):
		self.delete()

class Lecture(TimeStampedModel):
	instructor = models.ForeignKey('accounts.Instructor')
	university = models.ForeignKey(University)
	department = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	year = models.PositiveIntegerField(default=date.today().year)
	code = models.PositiveIntegerField(default=0)
	registration_code = RandomSlugField(length=7)
	roster = models.ManyToManyField('accounts.Student', through='RegisteredLecture', blank=True)

	def __unicode__(self):
		return u'%s:%s %d' % (self.department, self.name, self.year)

	def enrollment_count(self):
		return len(self.roster.all())

	class Meta:
		verbose_name = 'Class'
		verbose_name_plural = 'Classes'
		unique_together = ('university', 'department', 'name', 'year', 'code')




