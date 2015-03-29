from django.db import models
from model_utils.models import TimeStampedModel


class Stat(TimeStampedModel):
	attention_span = models.DecimalField(max_digits=5, decimal_places=2, default=50.0)
