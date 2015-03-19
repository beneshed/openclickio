from django.apps import AppConfig

class AccountsAppConfig(AppConfig):
	name = 'Accounts'

	def ready(self):
		import signals