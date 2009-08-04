from django.contrib import admin

from activitystreams.models import Source, Action, Activity, ActivityObject, Interest

admin.site.register(Source)
admin.site.register(Action)
admin.site.register(Activity)
admin.site.register(ActivityObject)
admin.site.register(Interest)
