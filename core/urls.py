from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from .views import StudentListLectureView, InstructorListLectureView, RegisteredLectureCreateView, CreateLectureView, LectureDetailView

urlpatterns = patterns('',
    url(r'^instructor/$', InstructorListLectureView.as_view(), name='instructor-class-list'),
    url(r'^student/$', StudentListLectureView.as_view(), name='student-class-list'),
    url(r'^lecture/register/$',RegisteredLectureCreateView.as_view(), name='register-lecture'),
    url(r'^lecture/create/$', CreateLectureView.as_view(), name='create-lecture'),
    url(r'^lecture/(?P<registration_code>[-_\w]+)/$', LectureDetailView, name='detail-lecture'),
)
