from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    # url(r'^book$', views.BookView.as_view(), name='book'),
]
