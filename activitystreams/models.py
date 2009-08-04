import datetime

from django.db import models
from django.db.models.query import Q
from django.contrib.auth.models import User

class Source(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Action(models.Model):
    source = models.ForeignKey(Source)
    slug = models.SlugField(unique=False)
    template = models.TextField()

    class Meta:
        unique_together = (('source', 'slug'),)

class ActivityObject(models.Model):
    source = models.ForeignKey(Source)
    content_type_id = models.PositiveIntegerField(null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = (('source', 'content_type_id', 'object_id'),)

class Activity(models.Model):
    action = models.ForeignKey(Action)
    user = models.ForeignKey(User)
    direct_object = models.ForeignKey(ActivityObject)
    indirect_object = models.ForeignKey(ActivityObject)
    timestamp = models.DateTimeField()

    content = models.TextField(blank=True)

    related_objects = models.ManyToManyFIeld(ActivityObject, through='RelatedActivityObject')

class RelatedActivityObject(models.Model):
    activity = models.ForeignKey(Activity)
    related_object = models.ForeignKey(ActivityObject)
    key = models.CharField(max_length=100)

    class Meta:
        unique_together = (('activityobject', 'related_object', 'key'),)

class ActivityDetail(models.Model):
    event = models.ForeignKey(Event, related_name='event_details')
    key = models.CharField(max_length=100)
    value = models.TextField()

    def __unicode__(self):
        return u'%s: %s' % (self.key, self.value)

    class Meta:
        unique_together = (('event', 'key'),)

class Interest(models.Model):
    activity_object = models.ForeignKey(ActivityObject)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = (('source_object', 'user'),)
