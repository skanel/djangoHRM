#####################################################################
# Project:    A*HRM
# Title:     Employee controller 
# Version:     0001
# Last-Modified:     2009-02-26 05:36:39  (Thu, 26 April 2009)        
# Author:     Sokha, Sin , Sanya, Mesa , Kanel (ALLWEB DEVELOPERS) 
# Status:     Active
# Type:     Process
# Created:     03-April-2009
# Post-History:     20-April-2009
######################################################################
from libs import *

from django.utils.translation import ugettext

@login_required
def search_employee(request):
    print "called"
    data = initialize_view(request)
    ses = request.session['AHRM_SESSION']
    com_id = ses.company_id
    search_criteria = SearchCriteria()
    '''
    Add the search criteria into the criteria object
    '''
    search_criteria.name = request.POST.get("search_name", "")
    search_criteria.marital_status = request.POST.get("search_status", "")
    if request.POST.get("search_active"):
        search_criteria.isActive =  int(request.POST.get("search_active", ""))
    if request.POST.get("search_nation"):
        search_criteria.nationality = int(request.POST.get("search_nation", ""))
    search_criteria.gender = request.POST.get("search_gender", "")
    if request.POST.get("search_dep"):
        search_criteria.department = int(request.POST.get("search_dep", ""))
    search_criteria.skill = request.POST.get("search_skill", "")
    if request.POST.get("search_language"):
        search_criteria.language = int(request.POST.get("search_language", ""))
    
    
    employees = Employee.objects.all()
    employees = employees.filter(company=com_id)
    if search_criteria.name:
        employees = employees.filter(fname__contains=request.POST.get("search_name")) | employees.filter(lname__contains=request.POST.get("search_name"))
    if search_criteria.marital_status:
        employees = employees.filter(marital_status=search_criteria.marital_status)
    if search_criteria.isActive != "":
        employees = employees.filter(active=search_criteria.isActive)
    if search_criteria.nationality:
        employees = employees.filter(nationality=search_criteria.nationality)
    if search_criteria.gender:
        employees = employees.filter(gender=search_criteria.gender)
    if search_criteria.skill:
        s = Skill.objects.all()
        s = s.filter(skill_name__contains = request.POST.get("search_skill")) | s.filter(description__contains = request.POST.get("search_skill"))
        list = []
        for skill in s:
           list.append(skill.employee_id)
           
        employees = employees.filter(id__in = list)
        
    if search_criteria.language:
        l = EmployeeLanguage.objects.extra(where=['language_id=%s'], params=[search_criteria.language])
        list = []
        for language in l:
            list.append(language.employee_id)
            
        employees = employees.filter(id__in = list)    
    
    if search_criteria.department:
        list_dep_id = dep_recursive(search_criteria.department, "")
        pos = EmployeePosition.objects.filter(department__in = list_dep_id)
    
        list = []
        for department in pos:
            list.append(department.employee_id)
        
        employees = employees.filter(id__in = list)
    
    data['departments'] = Department.objects.all()
    data['marital_status'] = MaritalStatus.objects.all()
    data['countries'] = Country.objects.all()
    data['gender'] = Gender.objects.all()
    data['criteria'] = search_criteria
    data['employees'] = employees.order_by('lname', 'fname')
    
    t = loader.get_template('employees/employee_search.html')
    c = Context(data)
    return HttpResponse(t.render(c))

def dep_recursive(id_department, list):
    if not list:
        list = [id_department]
    
    dep = Department.objects.all()
    dep = dep.filter(department_father = id_department)
    for d in dep:    
        list.append(d.id)
        dep_recursive(d.id, list)
    
      
    return list

def employee_save_emergency(request):
    status = "saved"
    return employee_create_emergency(request, "", status)

@login_required
def employee_create_emergency(request, emergency_id="", status=""):
    data = initialize_view(request)
    if request.method == "POST" and status == "saved":
        if request.POST.get("emer_id"):
            emergency_id = request.POST.get("emer_id")
        emp = Employee.objects.get(id = request.session['emp_id'])
        if emergency_id: 
            emergency = Emergency.objects.get(id = emergency_id)
        else:
            emergency = Emergency(employee = emp)
        form = forms.EmergencyForm(request.POST, instance = emergency)
        if form.is_valid():
            form.save()
            status = ""
            return HttpResponseRedirect('/employee/emergency')
    else:
        if emergency_id: 
            emergency = Emergency.objects.get(id = emergency_id)
            form = forms.EmergencyForm(instance = emergency)
        else:
            form = forms.EmergencyForm()
    emergencies = Emergency.objects.all()
    emergencies = emergencies.filter(employee = request.session['emp_id'])
    data['emp_tab'] = employee_tabs(request.session['emp_id'])
    data['emergency_id'] = emergency_id
    data['emergencies'] = emergencies
    data['form'] = form
    data['curr_employee'] = Employee.objects.get(id=request.session['emp_id'])
    data['tab_id'] = "emergency"
    data['status'] = status
    data['emp_id'] = request.session['emp_id']
    return render_to_response('employees/employee_main.html', data)
       
def employee_new_emergency(request):
    status = "new"
    return employee_create_emergency(request, "", status)
       
def employee_edit_emergency(request, emergency_id):
    status = "update"
    return employee_create_emergency(request, emergency_id, status) 

@login_required
def employee_delete_emergency(request, emergency_id):
    emergency = Emergency.objects.get(id = emergency_id)
    emergency.delete()
    return HttpResponseRedirect('/employee/emergency')

@login_required
def employee_create(request, employee_id="", status=""):
    data = initialize_view(request)
    nation = ""
    if not employee_id:
        if request.session['emp_id']:
            employee_id = request.session['emp_id']
    if request.method == "POST":
        com_id = data['company_id']
        com = Company.objects.get(id=com_id)
        emp = Employee(company=com)
        if not employee_id:
            if request.POST.get('emp_id'):
               employee_id = request.POST.get('emp_id')
        if employee_id != 'None' and  employee_id != '':
            emp = Employee.objects.get(id = employee_id)
        if request.POST.get("emp_nation"):
            country = Country.objects.get(id = request.POST.get("emp_nation"))
            nation = country.nationality 
        else:
            country = Country()
        emp.nationality = country
        
        
        
        form = forms.EmployeeForm(request.POST,request.FILES,instance=emp)
        if form.is_valid():
            if request.POST.get("emp_nation"):
                if employee_id!='' and emp.photo and request.FILES :
                   if os.path.isfile(emp.photo.path):
                      os.remove(emp.photo.path)
                  
                emp = form.save()                
                nation = country.nationality
            else:
                data['nation_error'] = "<font color='red'> Nationality: The nationality is mandatory.</font>"
            request.session['emp_id'] = emp.id
            employee_id = emp.id
    else:
        if employee_id:
            emp = Employee.objects.get(id = employee_id)
            country = Country.objects.get(id = emp.nationality_id)
            nation = country.nationality 
            form = forms.EmployeeForm(instance=emp)
        else:            
            form = forms.EmployeeForm()
    
    employees = Employee.objects.all() 
    
    data['country'] = Country.objects.all()
    data['nation'] = nation
    data['emp_id'] = employee_id
    if employee_id != '' :
        data['curr_employee'] = emp
    data['emp_tab'] = employee_tabs(employee_id)
    data['form'] = form
    data['tab_id'] = "personal"
    
#    #Start the pagination
#    paginator = Paginator(employees, 1) # Show 25 contacts per page
#
#    # Make sure page request is an int. If not, deliver first page.
#    try:
#        page = int(request.GET.get('page', '1'))
#    except ValueError:
#        page = 1
#
#    # If page request (9999) is out of range, deliver last page of results.
#    try:
#        employee = paginator.page(page)
#    except (EmptyPage, InvalidPage):
#        employee = paginator.page(paginator.num_pages)

    
    
    return render_to_response('employees/employee_main.html', data)

@login_required
def employee_edit(request, employee_id):
    if not request.session.has_key('emp_id'):
        request.session['emp_id'] = ""
    request.session['emp_id'] = employee_id
    return employee_create(request, employee_id, "edit")
   
@login_required
def employee_delete(request, employee_id):
    data = initialize_view(request)
    employee = Employee.objects.get(id=employee_id)
    employee.delete()
    return HttpResponseRedirect('/employee/search')

@login_required
def employee_department_delete(request, emp_dep_id):
    emp_dep = EmployeePosition.objects.get(id=emp_dep_id)
    emp_dep.delete()
    return HttpResponsePermanentRedirect("/employee/department")
@login_required
def employees_contacts_list(request):
    data = initialize_view(request)
    ses = request.session['AHRM_SESSION']
    com_id = ses.company_id
    
    employees = Employee.objects.filter(company=com_id).order_by('fname', 'lname')
    
    data['employees'] = employees
    #data['i'] = 0
    return render_to_response('employees/contacts_list.html', data)

@login_required
def employee_create_education(request, education_id="", status=""):
    data = initialize_view(request)
    if request.method == "POST" and status == "saved":
        if request.POST.get("education_id"):
            education_id = request.POST.get("education_id")
        emp = Employee.objects.get(id = request.session['emp_id'])
        if education_id:
            education = Education.objects.get(id = education_id)
        else:
            education = Education(employee = emp)
        form = forms.EducationForm(request.POST, instance = education)
        if form.is_valid():
            form.save()
            status = ""
            return HttpResponseRedirect('/employee/education')
    else:
        if education_id:
            education = Education.objects.get(id = education_id)
            form = forms.EducationForm(instance = education)
        else:
            form = forms.EducationForm()
            
    educations = Education.objects.all()
    educations = educations.filter(employee = request.session['emp_id'])
    
    '''Fill in the data need to send to view '''
    data['emp_tab'] = employee_tabs(request.session['emp_id'])
    data['education_id'] = education_id
    data['educations'] = educations
    data['tab_id'] = "education"
    data['status'] = status        
    data['form'] = form
    data['emp_id'] = request.session['emp_id']
    data['curr_employee'] = Employee.objects.get(id=request.session['emp_id'])
    return render_to_response('employees/employee_main.html', data)

def employee_new_education(request):
    return employee_create_education(request, "", "new")

def employee_save_education(request):
    return employee_create_education(request, "", "saved")

@login_required
def employee_delete_education(request, education_id):
    education = Education.objects.get(id = education_id).delete()
    return HttpResponseRedirect('/employee/education')

def employee_edit_education(request, education_id):
    return employee_create_education(request, education_id, "edit")

@login_required
def employee_create_skill(request, skill_id="", status=""):
    data = initialize_view(request)
    if request.method == "POST" and status == "saved":
        if request.POST.get("skill_id"):
            skill_id = request.POST.get("skill_id")
        emp = Employee.objects.get(id = request.session['emp_id'])
        if skill_id:
            skill = Skill.objects.get(id = skill_id)
        else:
            skill = Skill(employee = emp)
        form = forms.SkillForm(request.POST, instance = skill)
        if form.is_valid():
            form.save()
            status = ""
            return HttpResponseRedirect('/employee/skill')
    else:
        if skill_id:
            skill = Skill.objects.get(id = skill_id)
            form = forms.SkillForm(instance = skill)
     
        else:
            form = forms.SkillForm()
            
    skills = Skill.objects.all()
    skills = skills.filter(employee = request.session['emp_id'])
    
    '''Fill in the data need to send to view '''
    data['skill_id'] = skill_id
    data['skills'] = skills
    data['tab_id'] = "skill"
    data['status'] = status       
    data['form'] = form
    data['emp_id'] = request.session['emp_id']
    data['emp_tab'] = employee_tabs(request.session['emp_id'])
    data['curr_employee'] = Employee.objects.get(id=request.session['emp_id'])
    return render_to_response('employees/employee_main.html', data)

def employee_new_skill(request):
    return employee_create_skill(request, "", "new")

def employee_save_skill(request):
    return employee_create_skill(request, "", "saved")

def employee_edit_skill(request, skill_id):
    return employee_create_skill(request, skill_id, "update")

@login_required
def employee_delete_skill(request, skill_id):
    skill = Skill.objects.get(id = skill_id)
    skill.delete()
    return HttpResponseRedirect('/employee/skill')

@login_required
def employee_create_attachment(request, atch_id="", status=""):
    data = initialize_view(request)
    if request.method == "POST" and status == "saved":
        if request.POST.get("atch_id"):
            atch_id = request.POST.get("atch_id")
        emp = Employee.objects.get(id = request.session['emp_id'])
        if atch_id:
            attachment = Attachment.objects.get(id = atch_id)
        else:
            attachment = Attachment(employee = emp)
        form = forms.AttachmentForm(request.POST,request.FILES,instance = attachment)
        if form.is_valid():
            if atch_id!="" and attachment.content and request.FILES:
                if os.path.isfile(attachment.content.path):
                   os.remove(attachment.content.path)  
            form.save()
            status = ""
            return HttpResponseRedirect('/employee/attachment')
    else:
        if atch_id:
            attachment = Attachment.objects.get(id = atch_id)
            form = forms.AttachmentForm(instance = attachment)
     
        else:
            form = forms.AttachmentForm()
            
    attachments = Attachment.objects.all()
    attachments = attachments.filter(employee = request.session['emp_id'])
    
    '''Fill in the data need to send to view '''
    data['atch_id'] = atch_id
    data['attachments'] = attachments
    data['tab_id'] = "attachment"
    data['status'] = status       
    data['form'] = form
    data['emp_id'] = request.session['emp_id']
    data['emp_tab'] = employee_tabs(request.session['emp_id'])
    data['curr_employee'] = Employee.objects.get(id=request.session['emp_id'])
    return render_to_response('employees/employee_main.html', data)

def employee_new_attachment(request):
    return employee_create_attachment(request, "", "new")

def employee_save_attachment(request):
    return employee_create_attachment(request, "", "saved")

def employee_edit_attachment(request, atch_id):
    return employee_create_attachment(request, atch_id, "update")

@login_required
def employee_delete_attachment(request, atch_id):
    attachment = Attachment.objects.get(id = atch_id)
    attachment.delete()
    return HttpResponseRedirect('/employee/attachment')
    
def employee_tabs(emp_id):
    tabs = Tabs()
    personal = TabElement('personal', ugettext('Personal Infor'), '/employee/edit/' + str(emp_id), 'employees/employee_create_in_dept.html')
    department = TabElement('department', ugettext('Department'), '/employee/department', 'employees/employee_departement.html')
    emergency = TabElement('emergency', ugettext('Emergency'), '/employee/emergency', 'employees/employee_emergency.html')
    experience = TabElement('experience', ugettext('Experience'), '/employee/experience', 'employees/employee_experience.html')
    education = TabElement('education', ugettext('Education'), '/employee/education', 'employees/employee_education.html')
    skill = TabElement('skill', ugettext('Skill'), '/employee/skill', 'employees/employee_skill.html')
    language = TabElement('language', ugettext('Language'), '/employee/languages', 'employees/employee_language.html')
    attachment = TabElement('attachment', ugettext('Attachment'), '/employee/attachment', 'employees/employee_attachment.html')
    
    tabs.add_element(personal)
    tabs.add_element(department)
    tabs.add_element(emergency)
    tabs.add_element(experience)
    tabs.add_element(education)
    tabs.add_element(skill)
    tabs.add_element(language)
    tabs.add_element(attachment)
    
    return tabs

@login_required
def employee_create_language(request, emp_lang_id="", status=""):
    data = initialize_view(request)
    language = ""
    if request.method == "POST" and status == "saved":
        if request.POST.get("emp_lang_id"):
            emp_lang_id = request.POST.get("emp_lang_id")
        emp = Employee.objects.get(id = request.session['emp_id'])
        if emp_lang_id != 'None' and  emp_lang_id != '':
           employee_lang  = EmployeeLanguage.objects.get(id = emp_lang_id)
           
        else:
            employee_lang = EmployeeLanguage(employee = emp)
            
        if request.POST.get('emp_lang'):
           country = Country.objects.get(id = request.POST.get("emp_lang"))
           language = country.language
        else: 
           country = Country()
        employee_lang.language = country
        form = forms.EmployeeLanguageForm(request.POST, instance = employee_lang)
        if not request.POST.get('emp_lang'):
            data['lang_error'] = "<font color='red'> Nationality: The nationality is mandatory.</font>"
            
        if form.is_valid():
            if request.POST.get('emp_lang'):
                form.save()
                status = ""
                return HttpResponseRedirect('/employee/languages')
            
    else:
        if emp_lang_id:
            employee_lang = EmployeeLanguage.objects.get(id = emp_lang_id)
            country = Country.objects.get(id = employee_lang.language_id)
            language = country.language 
            form = forms.EmployeeLanguageForm(instance = employee_lang)
     
        else:
            form = forms.EmployeeLanguageForm()
            
    employee_langs = EmployeeLanguage.objects.all()
    employee_langs = employee_langs.filter(employee = request.session['emp_id'])
    
    '''Fill in the data need to send to view '''
    data['country'] = Country.objects.all()
    data['language'] = language
    data['emp_lang_id'] = emp_lang_id
    data['employee_langs'] = employee_langs
    data['tab_id'] = "language"
    data['status'] = status       
    data['form'] = form
    data['emp_id'] = request.session['emp_id']
    data['emp_tab'] = employee_tabs(request.session['emp_id'])
    data['curr_employee'] = Employee.objects.get(id=request.session['emp_id'])
    return render_to_response('employees/employee_main.html', data)

def employee_new_language(request):
    return employee_create_language(request, "", "new")

def employee_save_language(request):
    return employee_create_language(request, "", "saved")

def employee_edit_language(request, emp_lang_id):
    return employee_create_language(request, emp_lang_id, "edit")

@login_required
def employee_delete_language(request, emp_lang_id):
    emp_lang = EmployeeLanguage.objects.get(id = emp_lang_id)
    emp_lang.delete()
    return HttpResponseRedirect('/employee/languages')

def employee_department(request):
    return employee_department_modification_page(request, '')

def employee_department_new(request):
    return employee_department_modification_page(request, 'edit_save')

def employee_department_save(request):
    emp_dep_id = 0
    if (request.POST.has_key('curr_emp_dep_id')) :
        emp_dep_id = int(request.POST['curr_emp_dep_id'])
    return employee_department_modification_page(request, 'edit_save', emp_dep_id)

def employee_department_edit(request, emp_dep_id):
    return employee_department_modification_page(request, 'edit_save', emp_dep_id)

@login_required
def employee_department_modification_page(request, process, emp_dep_id=0):
    data = initialize_view(request)
    if process != '':
        if (request.method == "POST" and request.POST.has_key('btn_save')):
            dep_id = request.POST['department']
            pos_id = request.POST['position']
            if emp_dep_id != 0 :
                emp_dep = EmployeePosition.objects.get(id=emp_dep_id)
            else :
                emp_dep = EmployeePosition()
                emp_dep.employee_id = request.session['emp_id']
            emp_dep.position_id = pos_id
            if dep_id != 0 :
                 emp_dep.department_id = dep_id
            
            emp_dep.save()
            return HttpResponsePermanentRedirect("/employee/department")
        elif emp_dep_id != 0 :
            emp_dep = EmployeePosition.objects.get(id=emp_dep_id)
            data['curr_dep_id'] = emp_dep.department_id
            data['curr_pos_id'] = emp_dep.position_id
        else :
            dep_list = EmployeePosition.objects.filter(employee=request.session['emp_id'])
            data['emp_dep_list'] = dep_list
    else :
        dep_list = EmployeePosition.objects.filter(employee=request.session['emp_id'])
        data['emp_dep_list'] = dep_list
    data['curr_emp_dep_id'] = emp_dep_id
    positions = Position.objects.filter(company=data['company_id'])
    departments = Department.objects.filter(company=data['company_id'])
    
    data['status'] = process
    data['positions'] = positions
    data['departments'] = departments
    data['curr_employee'] = Employee.objects.get(id=request.session['emp_id'])
    data['tab_id'] = "department"
    data['emp_id'] = request.session['emp_id']
    data['emp_tab'] = employee_tabs(request.session['emp_id'])
    return render_to_response('employees/employee_main.html', data)

''' Goto employee creation page '''
@login_required
def goto_newemployee(request):
    request.session['emp_id'] = ""    
    return HttpResponsePermanentRedirect("/employee/new")    
