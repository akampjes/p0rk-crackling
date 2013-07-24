from django.conf.urls import patterns, include, url

urlpatterns = patterns('porkweb.views',
	url(r'^job/(?P<jobid>\d+)/$', 'front'),
	url(r"^$", "front"),
)
