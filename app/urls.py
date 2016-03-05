from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login$', views.login_user, name='login'),
    url(r'^logout$', views.logout_user, name='logout'),
    url(r'^signup$', views.signup_user, name='signup'),
    # logged in app
    url(r'^albums$', views.albums, name='albums'),
    url(r'^favoriates$', views.favorites, name='favorites'),
]
