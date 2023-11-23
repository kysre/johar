from django.contrib import admin

from news.models import Subscriber, Reporter, Agency, Category, News  #,  Like, DisLike, Comment

admin.site.register(Subscriber)


class ReporterInlineAdmin(admin.StackedInline):
    model = Reporter
    fields = ['user']
    extra = 1


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['names']
    inlines = [ReporterInlineAdmin]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'created_time']
    search_fields = ['titles']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'agency', 'author', 'image', 'description', 'is_draft']
    list_filter = ['agency', 'author', 'is_draft', 'categories']
    filter_horizontal = ['categories']
    search_fields = ['titles']


@admin.register(Reporter)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'avatar', 'agency']

