from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^images$', views.images, name='images'),
    url(r'^(?P<image_id>[0-9]+)/$', views.image, name='image'),
]