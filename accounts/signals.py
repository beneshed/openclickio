from django.contrib.auth.models import User
from django_cas_ng.signals import cas_user_authenticated
from django.dispatch import receiver
from django.db.models.signals import post_save
from registration.models import Registration
from django.conf import settings

@receiver(cas_user_authenticated)
def callback(sender, user, **kwargs):
	try:
		User.objects.get(username=user)
	except User.DoesNotExist:
		Registration.objects.create_inactive_user(user.username)

@receiver(post_save, sender=User)
def check_user(sender, instance, signal, created, **kwargs):
	if created and instance.is_superuser == False:
		instance.is_active = False
		instance.email = "%s@%s" % (instance.username, settings.ORGANIZATION_EMAIL_DOMAIN)
		instance.save()
		Registration.objects.create_registration(instance)



