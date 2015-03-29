from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test
from core.views import HomePageView, DashboardView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cs490.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^registration/', include('registration.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^classes/', include('core.urls')),
    #url(r'^qa/', include('qa.urls')),
    url(r'^$', HomePageView.as_view(), name='homepage'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),

)
