from django.contrib import admin

# Register your models here.
from feedback.models import Reaction, Comment


# admin.site.register(Reaction)

@admin.register(Reaction)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['news', 'subscriber', 'reactionType']
    list_filter = ['news', 'subscriber', 'reactionType']

@admin.register(Comment)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['news', 'subscriber', 'text']
    list_filter = ['news', 'subscriber', 'text']