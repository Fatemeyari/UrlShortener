from django.contrib import admin
from requests.compat import has_simplejson

from .models import User ,Profile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_display = ('phone_number'  ,'show_fullname','show_effective_url_limit' ,'is_superuser','is_staff','is_active',
                    'created_time')

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
    show_fullname.short_description = "Full Name"


    def show_effective_url_limit(self, obj):
        if hasattr(obj, 'profile') and obj.profile:
            return obj.profile.effective_url_limit
        return "-"
    show_effective_url_limit.short_description = "URL Limit"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_display = ('show_phone_number','full_name','show_is_active','show_is_superuser','show_is_staff',
                    'is_premium','created_time')
    fieldsets = [
        ('Information of Profile', {
            'fields': ('user', 'full_name', 'avatar', 'bio','website','is_premium','created_time','updated_time')
        })
    ]
    readonly_fields = ['created_time' , 'updated_time']
    list_filter = ['full_name','is_premium','user__is_active' , 'user__is_staff' , 'user__is_superuser']
    search_fields = ['full_name','user__phone_number','user__email']
    empty_value_display='empty'



    def show_phone_number(self , obj):
        if hasattr(obj , 'user') and obj.user:
            return obj.user.phone_number
        return '-'
    show_phone_number.short_description = "Phone Number"

    def show_is_active(self , obj ):
        if hasattr(obj,'user') and obj.user:
            return obj.user.is_active
        return '-'
    show_is_active.short_description = "Active"

    def show_is_superuser(self, obj):
        if hasattr(obj, 'user') and obj.user:
            return obj.user.is_superuser
        return '-'
    show_is_superuser.short_description = "Superuser"

    def show_is_staff(self, obj):
        if hasattr(obj, 'user') and obj.user:
            return obj.user.is_staff
        return '-'
    show_is_staff.short_description = "Staff"



