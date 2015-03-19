from django.conf.urls import patterns, include, url
from .views import ActivationView, StudentRegistrationView, InstructorRegistrationView

urlpatterns = patterns('',
    url(r'^activate/(?P<activation_key>\w+)/$', ActivationView.as_view(), name='activation-activate'),
    url(r'^student/$', StudentRegistrationView.as_view(), name='register-student'),
    url(r'^instructor/$', InstructorRegistrationView.as_view(), name='register-instructor'),
)
