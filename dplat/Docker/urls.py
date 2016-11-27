from django.conf.urls import url
from . import views
from django.conf import settings

app_name='Docker'

urlpatterns=[
url(r'^home',views.home_page,name='home_page'),
url(r'^register',views.register,name='register'),
# url(r'^/utility',views.utility,name='utiltiy'),
]
