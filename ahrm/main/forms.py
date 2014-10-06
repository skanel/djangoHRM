#####################################################################
# Project:    A*HRM
# Title:     Form controller 
# Version:     0001
# Last-Modified:     2009-02-26 05:36:39  (Thu, 26 April 2009)        
# Author:     Sokha, Sin , Sanya, Mesa , Kanel (ALLWEB DEVELOPERS) 
# Status:     Active
# Type:     Process
# Created:     03-April-2009
# Post-History:     20-April-2009
######################################################################
from django.forms import ModelForm
from ahrm.main.models import Employee, Company, Emergency, Experience, Department ,\
Education, Skill, Attachment, EmployeeLanguage, Country, ModelType, Position
from django.contrib.auth.models import User

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['fname', 'lname', 'birthday', 'marital_status', 'gender', 'photo',
                  'driver_licence', 'date_joined', 'street',
                  'city', 'zip_code', 'phone', 'mail', 'active']

class EmergencyForm(ModelForm):
    class Meta:
        model = Emergency
        exclude = ('employee')
        
class CompanyForm(ModelForm):
    class Meta:
        model = Company
        exclude = ('name')
     
class DepartmentForm(ModelForm):
    class Meta:
        model = Department       
        exclude = ("department_father","company","order_id")
        
class TypeForm(ModelForm):
    class Meta:
        model = ModelType   
    
class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ['start_date', 'end_date', 'position', 'mission', 'location']    
        
    
class UserForm(ModelForm):
    class Meta :
        model = User
        fields=['first_name', 'last_name', 'email']
        
class EducationForm(ModelForm):
    class Meta:
        model = Education
        exclude = ("employee")
        
class SkillForm(ModelForm):
    class Meta:
        model = Skill
        exclude = ("employee")
        
class AttachmentForm(ModelForm):
    class Meta:
        model = Attachment
        fields=['name', 'description', 'content']

class EmployeeLanguageForm(ModelForm):
    class Meta:
        model = EmployeeLanguage
        exclude = ("employee", "language")

class PositionForm(ModelForm):
    class Meta:
        model = Position
        exclude = ('company')