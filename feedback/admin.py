from django.contrib import admin

# Register your models here.
from feedback.models import Reaction

# admin.site.register(Reaction)

@admin.register(Reaction)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['news', 'subscriber', 'reaction']
    list_filter = ['news', 'subscriber', 'reaction']
