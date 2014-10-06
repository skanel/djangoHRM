################################################################### #
# Project:    A*HRM                                                 #
# Title:     Class Models of A*HRM Database (PostgrSQL)             #  
# Version:     0001                                                 #
# Last-Modified:     2009-02-26 05:36:39  (Thu, 26 Feb 2009)        #
# Author:     Sokha, Sin , Sanya, Mesa ,Kanel (ALLWEB DEVELOPERS)   #
# Status:     Active                                                #
# Type:     Process                                                 #
# Created:     20-Feb-2009                                          #
# Post-History:     03-Feb-2009                                     #
#####################################################################

from django.db import models
from django.contrib.auth.models import User
from django import forms as forms
from django.forms.widgets import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import datetime, time
from tinymce import models as tinymce_models
from django.utils.translation import ugettext_lazy



class Country(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
   
class Gender(models.Model):
    code = models.CharField(max_length=1, primary_key=True)
    desc = models.CharField(max_length=10)
    def __unicode__(self):
        return self.desc

class Company(models.Model):
    desc = models.CharField(ugettext_lazy('Description'),max_length=255)
    name = models.CharField(ugettext_lazy('Name'),max_length=40, )
    address = models.CharField(ugettext_lazy('Address'),max_length=500)
    city = models.CharField(ugettext_lazy('City'),max_length=100, blank=True, null=True)
    zipcode = models.CharField(ugettext_lazy('Zip code'),max_length=5, blank=True, null=True)
    phone1 = models.CharField(ugettext_lazy('Phone1'),max_length=20, blank=True, null=True)
    phone2 = models.CharField(ugettext_lazy('Phone2'),max_length=20, blank=True, null=True)
    mail = models.EmailField(ugettext_lazy('E-mail'),max_length=40, blank=True, null=True)
    welcome_message = tinymce_models.HTMLField(blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name=ugettext_lazy('Country'))
    logo = models.ImageField(upload_to="images/company_logo/", blank=True, help_text="Should be 50px wide")
    banner = models.ImageField(upload_to="images/company_banner/", blank=True, null=True)
    def __unicode__(self):
        return self.name
    
    def get_name(self):
        return self.name

class UserCompany(models.Model):
    company = models.ForeignKey(Company)
    user = models.ForeignKey(User)
    
class ModelType(models.Model):
    type_code = models.CharField(max_length=50, primary_key=True)
    type_desc = models.CharField(max_length=100)
    def __unicode__(self):
        return self.type_desc
        
class Department(models.Model):
    name = models.CharField(ugettext_lazy('Name'),max_length=50)
    desc = models.CharField(ugettext_lazy('Description'),max_length=200)    
    department_father = models.ForeignKey('self', blank=True, null=True)
    company = models.ForeignKey(Company)
    type = models.ForeignKey(ModelType)
    order_id = models.IntegerField()
    def __unicode__(self):        
        return "%s (%s)" % (self.name, self.company)
        

#This indicate the marital status   
class MaritalStatus(models.Model):
    code = models.CharField(max_length=5)
    desc = models.TextField(ugettext_lazy('Description'),max_length=200)    
    def __unicode__(self):        
        return self.desc
    

class Employee(models.Model):
    lname = models.CharField(ugettext_lazy('Last name'),max_length=200)    
    fname = models.CharField(ugettext_lazy('First name'),max_length=200)
    birthday = models.DateField(ugettext_lazy('Birthday'))
    marital_status = models.ForeignKey(MaritalStatus, verbose_name=ugettext_lazy('Marital Status'))
    driver_licence = models.CharField(ugettext_lazy('Driver licence'),max_length=50, blank=True, null=True)
    street = models.CharField(ugettext_lazy('Street'),max_length=50, blank=True, null=True)
    city = models.CharField(ugettext_lazy('City'),max_length=100)
    zip_code = models.CharField(ugettext_lazy('Zip code'),max_length=5)
    phone = models.CharField(ugettext_lazy('Phone'),max_length=20, blank=True)
    mail = models.EmailField(ugettext_lazy('E-mail'),max_length=40, blank=True)
    date_joined = models.DateField(ugettext_lazy('Date joined'))
    photo = models.ImageField(upload_to="images/photo/", blank=True, help_text="Should be 50px wide")
    active = models.BooleanField(ugettext_lazy('Active'))
    nationality = models.ForeignKey(Country)
    gender = models.ForeignKey(Gender, verbose_name=ugettext_lazy('Gender'))
    #department = models.ForeignKey(Department, blank=True, null=True)
    company = models.ForeignKey(Company, blank=False, null=False)
    def __unicode__(self):
        return "%s (%s)" % (self.lname, self.fname)
    def get_fullname(self):
       
        return ('%s %s' % (self.fname.upper(),self.lname))        
    get_fullname.short_description = 'Fullname'
    
    def photo_thumb(self):
        if self.photo:
            return '<img src="/%s/%s"></a>' % (settings.MEDIA_ROOT,self.photo)
        return None
    
    def get_age(self):
        current_date = time.localtime()
        birth_date = self.birthday.timetuple()
        
        d_year = current_date[0] - birth_date[0]
        d_month = current_date[1] - birth_date[1]
        d_day = current_date[2] - birth_date[2]
        
        if d_day <0:
            d_day = d_day + 30
            d_month = d_month-1
        #checks if difference in month is negative when difference in day is positive
        if d_month < 0 :
            d_month = d_month + 12
            d_year =  d_year - 1
        #the age found is:  d_year years and d_month months and d_day days
        return d_year
    def first_department_position(self):
        emp_pos = EmployeePosition.objects.filter(employee=self.id)
        if len(emp_pos) >0 :
            return emp_pos[0] 
        else :
            return ""
    photo_thumb.allow_tags = True
    photo_thumb.short_description = 'photo(95px*130px)'
   

class Emergency(models.Model):
    lname = models.CharField(ugettext_lazy('Last name'),max_length=100)    
    fname = models.CharField(ugettext_lazy('First name'),max_length=100)
    phone = models.CharField(ugettext_lazy('Phone'),max_length=50)
    mail = models.EmailField(ugettext_lazy('E-mail'),max_length=50)
    relationship = models.CharField(ugettext_lazy('Relationship'),max_length=50)
    employee = models.ForeignKey(Employee)#A employee has many Emergencies
    
class Experience(models.Model):
    start_date = models.CharField(ugettext_lazy('Start date'),max_length=100,blank=True, null=True)
    end_date = models.CharField(ugettext_lazy('End date'),max_length=100,blank=True, null=True)
    position = models.CharField(ugettext_lazy('Position'),max_length=100, blank=False, null=False)
    mission = models.TextField(ugettext_lazy('Mission'),max_length=1000)
    location = models.CharField(ugettext_lazy('Location'),max_length=100)
    employee = models.ForeignKey(Employee)
    
class Education(models.Model):
    school = models.CharField(ugettext_lazy('School'),max_length=100)
    start_date = models.CharField(ugettext_lazy('End date'),max_length=100,blank=True, null=True)
    end_date = models.CharField(ugettext_lazy('Start date'),max_length=100,blank=True, null=True)
    specialist = models.CharField(ugettext_lazy('Specialist'),max_length=100)
    employee = models.ForeignKey(Employee)
    description = models.TextField(ugettext_lazy('Description'),max_length=1000)

class Skill(models.Model):
    skill_name = models.CharField(ugettext_lazy('Skill'),max_length=100)
    description = models.TextField(max_length=1000, blank=True, null=True)
    employee = models.ForeignKey(Employee)
    
class EmployeeLanguage(models.Model):
    employee = models.ForeignKey(Employee)
    language = models.ForeignKey(Country, verbose_name=ugettext_lazy('Language'))
    COMPETENCY_CHOICES = (('Poor', 'Poor'), ('Basic', 'Basic'), ('Good', 'Good'), ('Mother tongue', 'Mother tongue'))
    FLUENCY_CHOICES = (('Writing' ,'Writing'),('Speaking', 'Speaking'), ('Reading', 'Reading'))
    competency = models.CharField(ugettext_lazy('Competency'),max_length=1, choices=COMPETENCY_CHOICES)
    fluency = models.CharField(ugettext_lazy('Fluency'),max_length=1, choices=FLUENCY_CHOICES)
    def __unicode__(self):
        return self.language


class Position(models.Model):
    name = models.CharField(ugettext_lazy('Name'),max_length=100)
    description = models.CharField(ugettext_lazy('Description'),max_length=500)
    company = models.ForeignKey(Company, blank=False, null=False)
    def __unicode__(self):
        return self.name


class EmployeePosition(models.Model):
    employee = models.ForeignKey(Employee)
    position = models.ForeignKey(Position)
    department = models.ForeignKey(Department, blank=True, null=True)
    def __unicode__(self):
        return str(self.position) + ' - ' + str(self.department) 

class Attachment(models.Model):
    name = models.CharField(ugettext_lazy('Name'),max_length=50)
    description = models.CharField(ugettext_lazy('Description'),max_length=100)
    extension = models.CharField(max_length=10,blank=True, null=True)
    size = models.FloatField(blank=True, null=True)
    content = models.FileField(ugettext_lazy('Content'),upload_to='attachments')
    employee = models.ForeignKey(Employee)
    def get_file_name(self):
        return str(self.content)[len('attachments')+1:]
    
    def get_extension(self):
        str_content=str(self.content)
        return str_content[str_content.find('.'):]
        
    