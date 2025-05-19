from django.contrib import admin
from .models import Announcement, AnnouncementCategory

@admin.register(AnnouncementCategory)
class AnnouncementCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published_at', 'is_published', 'created_at')
    list_filter = ('is_published', 'category', 'author', 'published_at', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'published_at'
    ordering = ('-published_at', '-created_at')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'category', 'content')
        }),
        ('Publication', {
            'fields': ('is_published', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    actions = ['publish_announcements', 'unpublish_announcements']

    def publish_announcements(self, request, queryset):
        queryset.update(is_published=True)
    publish_announcements.short_description = "Mark selected announcements as published"

    def unpublish_announcements(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_announcements.short_description = "Mark selected announcements as unpublished"