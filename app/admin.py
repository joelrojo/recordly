from django.contrib import admin
from .models import Song, Artist, Album


class SongAdmin(admin.ModelAdmin):
    pass
admin.site.register(Song, SongAdmin)


class ArtistAdmin(admin.ModelAdmin):
    pass
admin.site.register(Artist, ArtistAdmin)


class AlbumAdmin(admin.ModelAdmin):
    pass
admin.site.register(Album, AlbumAdmin)
