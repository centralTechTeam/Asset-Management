from django.contrib import admin
from assets.models import (
    Assets,
    Asset_Type,
    Assign,
    Vendor,
    Employee,
    #Profile,
    )

class Asset(admin.ModelAdmin):
    list_display = ('Name','Quantity','Asset_State','LifeSpan','Employee','Vendor')
    search_fields = ('Name','Vendor',)
    #readonly_fields = ('LifeSpan','Asset_State')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class Employees(admin.ModelAdmin):
    list_display = ('Full_Name','Title','Departments','Phone','user')
    search_fields = ('Full_Name','Departments',)
    #readonly_fields = ('Title','Phone')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class Vendors(admin.ModelAdmin):
    list_display = ('Company_Name','Business','Address','Email','Phone','Country')
    search_fields = ('Company_Name','Address',)
    #readonly_fields = ('Phone','Country','Business',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Assets, Asset),
admin.site.register(Asset_Type),
admin.site.register(Vendor, Vendors),
admin.site.register(Assign),
admin.site.register(Employee, Employees),
#admin.site.register(Profile),
