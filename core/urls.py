from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from .views import StudentListLectureView, InstructorListLectureView, RegisteredLectureCreateView, CreateLectureView, \
	LectureDetailView, LectureListView, UserRegisteredLectureView, UserRegisteredLectureApproveView, \
	CreateAttendanceView, RosterDetailView, RegistrationDeleteView, StudentLectureDetailView

urlpatterns = patterns('',
    url(r'^instructor/$', InstructorListLectureView.as_view(), name='instructor-class-list'),
    url(r'^student/$', StudentListLectureView.as_view(), name='student-class-list'),
    url(r'^lecture/register/$',RegisteredLectureCreateView.as_view(), name='register-lecture'),
    url(r'^lecture/registration/(?P<pk>\d+)/delete/$', RegistrationDeleteView.as_view(), name='delete-registration'),
    url(r'^lecture/pending/(?P<pk>\d+)/(?P<approved>[-_\w]+)/$', UserRegisteredLectureApproveView.as_view(), name='approve-deny-lecture'),
    url(r'^lecture/create/$', CreateLectureView.as_view(), name='create-lecture'),
    url(r'^lecture/(?P<pk>[-_\w]+)/$', LectureDetailView.as_view(), name='detail-lecture'),
    url(r'^lecture/(?P<pk>[-_\w]+)/student/$', StudentLectureDetailView.as_view(), name='student-detail-lecture'),
    url(r'^lecture/(?P<pk>[-_\w]+)/create/attendance/$', CreateAttendanceView.as_view() , name='create-attendance'),
    url(r'^lecture/(?P<pk>[-_\w]+)/roster/$', RosterDetailView.as_view() , name='roster-detail'),
    url(r'^lectures/$', LectureListView.as_view(), name='list-all-lecture'),
    url(r'^lectures/user/$', UserRegisteredLectureView.as_view(), name='users-registered-classes'),
)
