"""dockPlat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include 
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from Platform import views

urlpatterns=[
    url(r'^admin/', admin.site.urls),
	url(r'^docker/$',views.login_user,name='login'),
	url(r'^docker/register/$',views.register_user,name='register'),
	url(r'^docker/dashboard/$',views.dashboard,name='dashboard'),
	url(r'^docker/dashboard/run/$',views.run_container,name='run'),
	url(r'^docker/dashboard/view/$',views.view_containers,name='view'),
	url(r'^docker/logout/$',views.logout_user,name='logout'),
	url(r'^docker/dashboard/view/all/$',views.view_all,name='all'),
	url(r'^docker/dashboard/view/exited/$',views.view_exited,name='exited'),
	url(r'^docker/dashboard/view/running/$',views.view_running,name='running'),
	url(r'^docker/dashboard/view/paused/$',views.view_paused,name='paused'),
	url(r'^docker/dashboard/manage$$',views.manage_container,name='manage'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
