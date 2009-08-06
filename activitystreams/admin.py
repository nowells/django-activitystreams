from django.contrib import admin

from activitystreams.models import Source, Action, Activity, ActivityObject, Interest, UserObject

class SourceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug',)
    list_editable = ('slug',)

class ActionAdmin(admin.ModelAdmin):
    list_display = ('source', 'slug',)
    list_editable = ('slug',)

admin.site.register(Source, SourceAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Activity)
admin.site.register(ActivityObject)
admin.site.register(Interest)
admin.site.register(UserObject)
