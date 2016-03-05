from __future__ import unicode_literals

from django.db import models


class Song(models.Model):
    key = models.CharField(max_length=8, unique=True, blank=True, null=True)
    title = models.CharField(max_length=250, unique=True, blank=True)
    favorited = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title or u''

    class Meta:
        app_label = 'app'


class Artist(models.Model):
    key = models.CharField(max_length=8, unique=True, blank=True, null=True)
    name = models.CharField(max_length=250, unique=True, blank=True)
    favorited = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name or u''

    class Meta:
        app_label = 'app'


class Album(models.Model):
    key = models.CharField(max_length=8, unique=True, blank=True, null=True)
    title = models.CharField(max_length=250, unique=True, blank=True)
    favorited = models.BooleanField(default=False)
    songs = models.ManyToManyField(Song, blank=True)
    artist = models.ForeignKey(Artist, blank=True)

    def __unicode__(self):
        return self.title or u''

    class Meta:
        app_label = 'app'
