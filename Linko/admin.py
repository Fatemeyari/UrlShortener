from django.contrib import admin

from .models import ShortURL , ClickStats

class ShorUrlInlineAdmin(admin.StackedInline):
    model=ShortURL
    extra=0

class ClickStatsInlineAdmin(admin.StackedInline):
    model=ClickStats
    extra=0

@admin.register(ShortURL)
class ShortUrlAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_display = [
        'show_user', 'show_email' , 'original_url' , 'short_code' , 'is_active'
    ]


    fieldsets = [
        ('Link Information', {
            'fields': ('user', 'original_url', 'short_code','clicks', 'is_active', 'custom_alias', 'qr_code')
        }),
        ('Date Information' , {
            'fields': ('created_time','expires_time','last_clicked')
        })

    ]
    readonly_fields = ['created_time', 'clicks', 'last_clicked']
    list_filter = ['user','is_active' , 'created_time','expires_time']
    search_fields = ['original_url', 'user__email', 'user__phone_number']
    empty_value_display='empty'
    inlines = [ClickStatsInlineAdmin]

    @admin.display(description='Phone Number')
    def show_user(self , obj):
        if hasattr(obj , 'user') and obj.user:
            return obj.user.phone_number
        return '-'

    @admin.display(description='Email')
    def show_email(self , obj):
        if hasattr(obj , 'user') and obj.user:
            return obj.user.email
        return '-'

