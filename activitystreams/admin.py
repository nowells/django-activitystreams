from django.contrib import admin

from activitystreams.models import Source, Action, Activity, ActivityObject, ActivityDetail, Interest

admin.site.register(Source)
admin.site.register(Action)
admin.site.register(Activity)
admin.site.register(ActivityDetail)
admin.site.register(ActivityObject)
admin.site.register(Interest)
