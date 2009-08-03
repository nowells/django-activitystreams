from django.db import models
from django.db.models.query import Q
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class EventType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    format = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class EventManager(models.Manager):
    def filter_for_event_object(self, obj):
        extra_id = 0
        content_type = ContentType.objects.get_for_model(obj)
        return self.extra(
                tables=['eventlogs_eventobject AS eventlogs_eventobject__user%s' % extra_id],
                where=[
                    'eventlogs_eventobject__user%s.event_id = eventlogs_event.id' % extra_id,
                    'eventlogs_eventobject__user%s.content_type_id = %%s' % extra_id,
                    'eventlogs_eventobject__user%s.object_id = %%s' % extra_id,
                    ],
                params=[content_type.id, obj._get_pk_val()]
                ).distinct()

    def filter_for_contexts(self, content_objects):
        query = None
        for obj in content_objects:
            content_type = ContentType.objects.get_for_model(obj)

            if query:
                query = query | (Q(context_content_type=content_type) & Q(context_object_id=obj._get_pk_val()))
            else:
                query = (Q(context_content_type=content_type) & Q(context_object_id=obj._get_pk_val()))

        if query:
            return self.filter(query)
        else:
            return self.none()
        
    def with_event_type(self):
        return self.extra(select={
                'event_type_name':"""
                    SELECT name FROM eventlogs_eventtype EET WHERE EET.id=eventlogs_event.event_type_id""",
            })

class Event(models.Model):
    event_type = models.ForeignKey(EventType, related_name='events')
    user = models.ForeignKey(User, blank=True, null=True)
    context_object = generic.GenericForeignKey('context_content_type', 'context_object_id')
    content_object = generic.GenericForeignKey()
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField()

    content_type = models.ForeignKey(ContentType, related_name='eventlogs_events', null=True, blank=True)
    object_id = models.PositiveIntegerField(db_index=True, null=True, blank=True)
    context_content_type = models.ForeignKey(ContentType, related_name='eventlogs_context_events', null=True, blank=True)
    context_object_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    objects = EventManager()

    def __unicode__(self):
        return u'%s: %s' % (self.event_type.name, self.summary)

    def set_user(self, user):
        self.user = None
        if isinstance(user, User):
            self.user = user

    def save(self):
        if not self.timestamp:
            self.timestamp = datetime.datetime.now()
        return super(Event, self).save()

    def get(self, key, default=None):
        results = self.getlist(key)
        if results:
            return results[0]
        return default

    def getlist(self, key):
        results = []
        if not hasattr(self, '_event_details'):
            self._event_details = self.event_details.all()

        for detail in self._event_details:
            if detail.key == key:
                results.append(detail.value)

        if not hasattr(self, '_event_objects'):
            self._event_objects = self.event_objects.all()

        for obj in self._event_objects:
            if obj.key == key:
                results.append(obj.content_object)

        return results

    class Meta:
        ordering = ('-timestamp',)

class EventDetail(models.Model):
    event = models.ForeignKey(Event, related_name='event_details')
    key = models.CharField(max_length=100)
    value = models.TextField()

    def __unicode__(self):
        return u'%s: %s' % (self.key, self.value)

class EventObject(models.Model):
    event = models.ForeignKey(Event, related_name='event_objects')
    key = models.CharField(max_length=100)
    content_object = generic.GenericForeignKey()

    content_type = models.ForeignKey(ContentType, related_name='eventlogs_event_objects')
    object_id = models.PositiveIntegerField(db_index=True)

    def __unicode__(self):
        return u'%s: %s %s' % (self.key, self.content_type, self.object_id)
