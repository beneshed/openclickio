from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from .views import InstructorCreateView, UserDetailView

urlpatterns = patterns('',
    url(r'^search/', include('haystack.urls')),
    url(r'^login/$', 'django_cas_ng.views.login', name='login'),
    url(r'^logout/$', 'django_cas_ng.views.logout', name='logout'),
    url(r'^new/$', TemplateView.as_view(template_name='new_account'), name='new-account'),
    url(r'^create/instructor/$', InstructorCreateView.as_view(), name='create-instructor'),
    url(r'^profile/(?P<pk>[-_\w]+)/$', UserDetailView.as_view(), name='user-detail'),
)
