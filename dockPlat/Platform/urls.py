from django.conf.urls import url
from . import views
from django.conf import settings

app_name='Docker'

urlpatterns=[
	url(r'^',views.login,name='login'),
	url(r'^register',views.register,name='register'),
	url(r'^dashboard',views.dashboard,name='dashboard'),
	url(r'^dashboard/run',views.run_container,name='run'),
	url(r'^dashboard/view',views.view_containers,name='view'),
	url(r'^logout',views.logout,name='logout'),
]
