from django.contrib import admin

from news.models import Subscriber, Agency, Category, News, Like, DisLike, Comment

admin.site.register(Subscriber)


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['parent', 'title', 'is_enable', 'created_time']
    list_filter = ['is_enable', 'parent']
    search_fields = ['titles']


class LikeInlineAdmin(admin.StackedInline):
    model = Like
    fields = ['user']
    extra = 1


class DisLikeInlineAdmin(admin.StackedInline):
    model = DisLike
    fields = ['user']
    extra = 1


class CommentInlineAdmin(admin.StackedInline):
    model = Comment
    fields = ['parent', 'user', 'description']
    extra = 1


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'agency', 'image', 'description', 'icon', 'is_enable']
    list_filter = ['agency', 'is_enable', 'categories']
    filter_horizontal = ['categories']
    search_fields = ['titles']
    inlines = [LikeInlineAdmin, DisLikeInlineAdmin, CommentInlineAdmin]
