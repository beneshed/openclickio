from haystack import indexes
from .models import Lecture


class LectureIndex(indexes.SearchIndex, indexes.Indexable):
	university = indexes.CharField(model_attr='university')
	department = indexes.CharField(model_attr='department')
	name = indexes.CharField(document=True, use_template=True)
	year = indexes.IntegerField(model_attr='year')

	def get_model(self):
		return Lecture

	def index_queryset(self, using=None):
		return self.get_model().objects.all()