from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from .views import InstructorCreateView, UserDetailView, PublicProfileView

urlpatterns = patterns('',
    url(r'^search/', include('haystack.urls')),
    url(r'^login/$', 'django_cas_ng.views.login', name='login'),
    url(r'^login/2/$', 'django.contrib.auth.views.login', {'template_name':'login.html'},  name='login-normal'),
    url(r'^logout/$', 'django_cas_ng.views.logout', name='logout'),
    url(r'^new/$', TemplateView.as_view(template_name='new_account.html'), name='new-account'),
    url(r'^create/instructor/$', InstructorCreateView.as_view(), name='create-instructor'),
    url(r'^profile/(?P<pk>[-_\w]+)/$', UserDetailView.as_view(), name='user-detail'),
    url(r'^public/profile/(?P<pk>[-_\w]+)/$', PublicProfileView, name='public-profile'),
)
