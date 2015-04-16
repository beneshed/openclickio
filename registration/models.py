from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template.loader import get_template
import hashlib, random, re
from django.conf import settings
from templated_email import send_templated_mail
import requests
from braces.views._access import AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.core.exceptions import ImproperlyConfigured, PermissionDenied


SHA256_RE = re.compile('^[a-f0-9]{40}$')


class RegistrationManager(models.Manager):

	def activate_user(self, activation_key):
		if SHA256_RE.search(activation_key):
			try:
				registration = self.get(activation_key=activation_key)
			except self.model.DoesNotExist:
				return False
			if not registration.activation_key.expired():
				user = registration.user
				user.is_active = True
				user.save()
				registration.verified = True
				registration.save()
				return user
			return False


	def create_registration(self, user):
		print 'creating registration'
		salt = hashlib.sha256(str(random.random())).hexdigest()[:5]
		username = user.username
		if isinstance(username, unicode):
			username = username.encode('utf-8')
		activation_key = hashlib.sha256(salt+username).hexdigest()
		self.create(user=user, activation_key=activation_key)
		self.send_activation_email(user)

	def send_activation_email(self, user):
		requests.post(
        "https://api.mailgun.net/v3/sandbox7c1396c8d3894cbba8d18c1e529898bc.mailgun.org/messages",
        auth=("api", "key-e2e3cf272cdfa26c74238ff2217a3537"),
        data={"from": "Mailgun Sandbox <postmaster@sandbox7c1396c8d3894cbba8d18c1e529898bc.mailgun.org>",
              "to": "<" + user.email + ">",
              "subject": "Hello Ben Waters",
              "text": "Congratulations: http://localhost:8000/registration/activate/" + user.registration.activation_key})


	def delete_expired_users(self):
		pass

class Registration(TimeStampedModel):
	user = models.OneToOneField(User, unique=True)
	verified = models.BooleanField(default=False)
	activation_key = models.CharField(max_length=255)
	objects = RegistrationManager()

	def __unicode__(self):
		return u"Registration information for %s" % self.user


class RegisteredMixin(AccessMixin):
	redirect_unauthenticated_users = False

	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_active:
			return redirect('homepage')
		return super(RegisteredMixin, self).dispatch(
            request, *args, **kwargs)
