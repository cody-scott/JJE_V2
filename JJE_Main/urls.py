from django.conf.urls import url, include
from JJE_Main import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index')
]