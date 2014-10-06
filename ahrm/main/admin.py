#####################################################################
# Project:    A*HRM
# Title:     Admin controller 
# Version:     0001
# Last-Modified:     2009-02-26 05:36:39  (Thu, 26 April 2009)        
# Author:     Sokha, Sin , Sanya, Mesa , Kanel (ALLWEB DEVELOPERS) 
# Status:     Active
# Type:     Process
# Created:     03-April-2009
# Post-History:     20-April-2009
######################################################################
from ahrm.main.models import Company, Department, Employee, Country, Gender, MaritalStatus,\
UserCompany, ModelType, Position, EmployeePosition, Attachment

from django.contrib import admin

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id','get_fullname', 'nationality','gender','birthday','photo_thumb')
    list_filter = ('gender',)
    search_fields = ('get_fullname',)
    ordering = ('id','lname',)
    list_display_links = ('get_fullname',)

class DepartmentAdmin(admin.ModelAdmin):
    fieldsets = [
         (None,             {'fields': ['name']}),
         (None,             {'fields': ['department_father']}), 
         (None,             {'fields': ['company']}),
         ('Description',    {'fields': ['desc'], 'classes':['collapse']}),
    ]

admin.site.register(Company)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Department,DepartmentAdmin)
admin.site.register(Country)
admin.site.register(Gender)
admin.site.register(MaritalStatus)

admin.site.register(UserCompany)
admin.site.register(Attachment)

#admin.site.register(UserCompany)
admin.site.register(Position)
admin.site.register(EmployeePosition)
#admin.site.register(UserCompany)
admin.site.register(ModelType)

