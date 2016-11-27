from django.conf.urls import url
from . import views
from django.conf import settings

app_name='Platform'

urlpatterns=[
	url(r'^',views.login,name='login'),
	url(r'^register',views.register_user,name='register'),
	url(r'^dashboard',views.dashboard,name='dashboard'),
	url(r'^dashboard/run',views.run_container,name='run'),
	url(r'^dashboard/view',views.view_containers,name='view'),
	url(r'^logout',views.logout,name='logout'),
	url(r'^dashboard/view/all',views.view_all,name='all'),
	url(r'^dashboard/view/exited',views.view_exited,name='exited'),
	url(r'^dashboard/view/running',views.view_running,name='running'),
]
