#####################################################################
# Project:    A*HRM
# Title:     libs controller 
# Version:     0001
# Last-Modified:     2009-02-26 05:36:39  (Thu, 26 April 2009)        
# Author:     Sokha, Sin , Sanya, Mesa , Kanel (ALLWEB DEVELOPERS) 
# Status:     Active
# Type:     Process
# Created:     03-April-2009
# Post-History:     20-April-2009
######################################################################
from ahrm.main.models import Company, Department, Employee, UserCompany,MaritalStatus, Country,\
Gender, Emergency, Experience,Education, Skill,EmployeeLanguage, Attachment, EmployeePosition,\
Position, ModelType
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, SetPasswordForm
from ahrm.main.helpers import UserCompanyRegister, AHRMSession, Tabs, TabElement
from django.http import HttpResponsePermanentRedirect, HttpResponseGone
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from main.search_criteria import SearchCriteria
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.contrib.auth.models import User, Group
from forms import UserForm, PositionForm, DepartmentForm
import forms
import os
from django.conf import settings

def initialize_view(request):
    user = request.user
    result = {'username':user.username}
    com_name = ''
    com_id = 0
    multi_companies = 0
    user_type = 0
    user_id = 0
    try:
        ses = request.session['AHRM_SESSION']
        com_name = ses.company_name
        com_id = ses.company_id
        multi_companies = ses.multi_companies 
        user_type = ses.user_type
        user_id = ses.user_id
    except KeyError:
        pass
    result['company_name'] = com_name
    result['company_id'] = com_id
    result['multi_companies'] = multi_companies
    result['user_type'] = user_type
    result['user_id'] = user_id
    result['LANGUAGES'] = settings.LANGUAGES
    return result; 
