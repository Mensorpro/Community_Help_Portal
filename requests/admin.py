from django.contrib import admin
from .models import RequestPost, Response

# Register your models here.
class RequestPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'requester', 'category', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'requester__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'requester', 'description', 'category', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) # Collapsible section
        }),
    )

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('request_post_title', 'responder', 'created_at')
    list_filter = ('created_at', 'responder__username')
    search_fields = ('message', 'request_post__title', 'responder__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def request_post_title(self, obj):
        return obj.request_post.title
    request_post_title.short_description = 'Request Post Title'

admin.site.register(RequestPost, RequestPostAdmin)
admin.site.register(Response, ResponseAdmin)
