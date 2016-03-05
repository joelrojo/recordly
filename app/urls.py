from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login$', views.login_user, name='login'),
    url(r'^logout$', views.logout_user, name='logout'),
    url(r'^signup$', views.signup_user, name='signup'),
    # logged in app
    url(r'^albums$', views.albums, name='albums'),
    url(r'^favorites$', views.favorites, name='favorites'),
    url(r'^album/(?P<key>\w{8})$', views.album_page, {}, 'album_page'),
    url(r'^song/(?P<key>\w{8})$', views.song_page, {}, 'song_page'),
    url(r'^artist/(?P<key>\w{8})$', views.artist_page, {}, 'artist_page'),

    url(r'^app/favorite$', views.favorite_item, {}, 'favorite_item'),
]
