from django.contrib import admin

from .models import User ,Profile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_display = ('phone_number'  ,'show_fullname','show_effective_url_limit' ,'is_superuser','is_staff','is_active','created_time')

    fieldsets = [
        ('Information of User' , {
            'fields':('phone_number','email','password','is_active','created_time','updated_time')
        }),
        ('Check SuperUser',{
            'fields':('is_superuser','is_staff')
        })

    ]
    readonly_fields = ['created_time' , 'updated_time']
    list_filter = ['is_superuser' , 'is_staff' , 'is_active']
    search_fields = ['phone_number' , 'email']
    empty_value_display='empty'

    def show_fullname(self , obj):
        if hasattr(obj, "profile") and obj.profile:
            return obj.profile.full_name
        return "-"


    def show_effective_url_limit(self, obj):
        if hasattr(obj, 'profile') and obj.profile:
            return obj.profile.effective_url_limit
        return "-"
    show_effective_url_limit.short_description = "URL Limit"

