"""
Model definitions to representation the activitystreams for multiple sites.
"""

import datetime

from django.db import models
from django.db.models.query import Q
from django.contrib.auth.models import User

class Source(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

class Action(models.Model):
    source = models.ForeignKey(Source, related_name='actions')
    slug = models.SlugField(unique=False)
    template = models.TextField()

    def __unicode__(self):
        return u'%s: %s' % (self.source, self.slug)

    class Meta:
        unique_together = (('source', 'slug'),)

class ActivityObject(models.Model):
    source = models.ForeignKey(Source, related_name='activity_objects')
    content_type_id = models.PositiveIntegerField(null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        return '%s:%s:%s' % (self.source, self.content_type_id, self.object_id)

    class Meta:
        unique_together = (('source', 'content_type_id', 'object_id'),)

class Activity(models.Model):
    action = models.ForeignKey(Action, related_name='activities')
    user = models.ForeignKey(User, related_name='activitystreams_activities')
    direct_object = models.ForeignKey(ActivityObject, related_name='direct_activities')
    indirect_object = models.ForeignKey(ActivityObject, related_name='indirect_activities')
    timestamp = models.DateTimeField()

    content = models.TextField(blank=True)

    related_objects = models.ManyToManyField(ActivityObject, through='RelatedActivityObject')

    def __unicode__(self):
        return '%s:%s:%s' % (self.action, self.user_id, self.id)

class RelatedActivityObject(models.Model):
    activity = models.ForeignKey(Activity)
    related_object = models.ForeignKey(ActivityObject)
    key = models.CharField(max_length=100)

    class Meta:
        unique_together = (('activity', 'related_object', 'key'),)

class ActivityDetail(models.Model):
    activity = models.ForeignKey(Activity, related_name='activity_details')
    key = models.CharField(max_length=100)
    value = models.TextField()

    def __unicode__(self):
        return u'%s: %s' % (self.key, self.value)

    class Meta:
        unique_together = (('activity', 'key'),)

class Interest(models.Model):
    activity_object = models.ForeignKey(ActivityObject, related_name='interests')
    user = models.ForeignKey(User, related_name='activitystreams_interests')

    class Meta:
        unique_together = (('activity_object', 'user'),)
