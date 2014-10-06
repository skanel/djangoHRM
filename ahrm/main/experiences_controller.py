#####################################################################
# Project:    A*HRM
# Title:     Experience controller 
# Version:     0001
# Last-Modified:     2009-02-26 05:36:39  (Thu, 26 April 2009)        
# Author:     Sokha, Sin , Sanya, Mesa , Kanel (ALLWEB DEVELOPERS) 
# Status:     Active
# Type:     Process
# Created:     03-April-2009
# Post-History:     20-April-2009
######################################################################
from employees_controller import employee_tabs
from libs import *

#@login_required
#def experience_save(request,experience_id="",process=""):
#    data = initialize_view(request)
#    if request.method == "POST" and request.POST.has_key('experience_save'):
#        emp = Employee.objects.get(id = request.session['emp_id'])
#        if experience_id !=0:
#            experience = Experience.objects.get(id = experience_id)
#        else:
#            experience = Experience(employee = emp)
#        form = forms.ExperienceForm(request.POST, instance = experience)
#        if form.is_valid():
#            form.save()
#            process = ""
#            return HttpResponseRedirect('/employee/experience')
#    else:
#        if experience_id !=0:
#            experience = Experience.objects.get(id = experience_id)
#            form = forms.ExperienceForm(instance = experience)
#        else:
#            form = forms.ExperienceForm()
#            
#    experiences = Experience.objects.all()
#    experiences = experiences.filter(employee=request.session['emp_id'])
#    data['emp_tab'] = employee_tabs(request.session['emp_id'])        
#    data['emp_id']=request.session['emp_id']
#    data['tab_id']='experience'
#    data['experience_id']=experience_id
#    data['form']=form
#    data['process']=process
#    data['experience_list']=experiences
#    data['curr_employee'] = Employee.objects.get(id=request.session['emp_id'])
#    return render_to_response('employees/employee_main.html', data)    

def experience_edit(request,exp_id):
    status = "update"
    return employee_create_experience(request, exp_id, status) 

def experience_new(request):
    status = "new"
    return employee_create_experience(request, "", status)
  
def employee_save_experience(request):
    status = "saved"
    return employee_create_experience(request, "", status)

@login_required
def experience_delete(request, exp_id):
    data = initialize_view(request)
    experience = Experience.objects.get(id=exp_id)
    experience.delete()
    return HttpResponseRedirect('/employee/experience')


@login_required
def employee_experience(request):
    return experience_save('employees/employee_main.html', data)


@login_required
def employee_create_experience(request, experience_id="", status=""):
    data = initialize_view(request)
    if request.method == "POST" and status == "saved":
        if request.POST.get("exp_id"):
            experience_id = request.POST.get("exp_id")
        emp = Employee.objects.get(id = request.session['emp_id'])
        if experience_id: 
            experience = Experience.objects.get(id = experience_id)
        else:
            experience = Experience(employee = emp)
        form = forms.ExperienceForm(request.POST, instance = experience)
        if form.is_valid():
            form.save()
            status = ""
            return HttpResponseRedirect('/employee/experience')
    else:
        if experience_id: 
            experience = Experience.objects.get(id = experience_id)
            form = forms.ExperienceForm(instance = experience)
        else:
            form = forms.ExperienceForm()
    experiences = Experience.objects.all()
    experiences = experiences.filter(employee = request.session['emp_id'])
    data['emp_tab'] = employee_tabs(request.session['emp_id'])
    data['experience_id'] = experience_id
    data['experiences'] = experiences
    data['form'] = form
    data['curr_employee'] = Employee.objects.get(id=request.session['emp_id'])
    data['tab_id'] = "experience"
    data['status'] = status
    data['emp_id'] = request.session['emp_id']
    return render_to_response('employees/employee_main.html', data)