#####################################################################
# Project:    A*HRM
# Title:     Department controller 
# Version:     0001
# Last-Modified:     2009-02-26 05:36:39  (Thu, 26 April 2009)        
# Author:     Sokha, Sin , Sanya, Mesa , Kanel (ALLWEB DEVELOPERS) 
# Status:     Active
# Type:     Process
# Created:     03-April-2009
# Post-History:     20-April-2009
######################################################################
from libs import *
from django.utils.translation import ugettext_lazy


@login_required
def department_display(request, dept_id):
    dept_result = Department.objects.filter(id=dept_id)
    if len(dept_result) != 1:
        raise Exception("Error while fetching department with id %s!" % dept_id)
    t = loader.get_template('display_department.html')
    c = Context({'department': dept_result[0]})
    return HttpResponse(t.render(c))

'''  Department creation '''
@login_required
def department_process(request):
    data = initialize_view(request)
    ses = request.session['AHRM_SESSION']
    data['id'] = ses.company_id   
    print request.POST
    if request.method == 'POST' and request.POST.has_key('dep_add'):
        print request.POST         
        if request.POST['type'] == 'Department':
            objDep = Department.objects.get(id=request.POST['id'])
            data['name'] = objDep.name
            data['dep_father_id'] = request.POST['id']
        elif request.POST['type'] == 'Company':        
            data['name'] = 'None'
            data['dep_father_id'] = 'None'
        objType = ModelType.objects.all() 
        data['company'] = ses.company_name
        data['dep_type'] = objType
        return render_to_response('departments/department_edit.html', data)
    elif request.method == 'POST' and request.POST.has_key('dep_delete'):
        objDepFather = Department.objects.get(id=request.POST['id'])
        objDepFather.delete()        
        return HttpResponseRedirect('/company/structure/')
    elif request.method == 'POST' and request.POST.has_key('dep_edit'):        
        dep = Department.objects.get(id=request.POST['id'])
        form = forms.DepartmentForm(instance=dep)                
        objType = ModelType.objects.all()
        data['dep_id'] = request.POST['id']
        data['company'] = ses.company_name
        data['dep_type'] = objType
        data['name'] = dep.department_father
        data['form'] = form        
        return render_to_response('departments/department_edit.html', data)
    
''' Saving department, this will be called by functions department_edit or department_new '''
@login_required
def department_save(request):
    data = initialize_view(request)
    ses = request.session['AHRM_SESSION']
    objData = Department()
    if request.POST['dep_name']!='' and request.POST['dep_desc']!='' :            
        objData.name = request.POST['dep_name']
        objData.desc = request.POST['dep_desc']    
        if request.POST['dep_father'] != 'None':
           objDepFather = Department.objects.get(id=request.POST['dep_father_id'])
        else :
           objDepFather = None      
        objData.department_father = objDepFather    
        objCompany = Company.objects.get(id=ses.company_id)
        objData.type = ModelType.objects.get(type_code=request.POST['dep_type'])
        objData.company = objCompany        
        args = Department.objects.all()
        max_index = 0 
        for dpt in args:
            if max_index < dpt.order_id:
                max_index = dpt.order_id           
        max_index = max_index + 1
        print max_index
        objData.order_id = max_index 
        objData.save()
        data['id'] = ses.company_id
        data['name'] = ses.company_name
        return render_to_response('companystructure.html', data)
    else :
        if request.POST['dep_name']=='':
            data['error_dep_name'] = ugettext_lazy('Department Name could not be blank')
        else:
            data['error_dep_name'] = ''
        if request.POST['dep_desc']=='':
            data['error_dep_desc'] = ugettext_lazy('Department Describtion could not be blank')
        else:
            data['error_dep_desc'] = ''                       
        data['id'] = ses.company_id
        data['name'] = request.POST['dep_father']
        data['dep_name'] = request.POST['dep_name']
        data['dep_desc'] = request.POST['dep_desc']
        objType = ModelType.objects.all() 
        data['company'] = request.POST['dep_com']
        data['dep_father_id'] = request.POST['dep_father_id']
        data['dep_type'] = objType 
        print data
        return render_to_response('departments/department_edit.html', data)

''' Updating department'''
@login_required
def department_update(request):      
    data = initialize_view(request)
    ses = request.session['AHRM_SESSION']   
    data['id'] = ses.company_id
    data['name'] = ses.company_name
    dep = Department.objects.get(id=request.POST['dep_id'])
    form = forms.DepartmentForm (request.POST, instance=dep)
    data['form'] = form            
    if form.is_valid() and dep.name != '':
        form.save()
        return render_to_response('companystructure.html', data)
    else :        
        data['dep_id'] = request.POST['dep_id'] 
        return render_to_response('departments/department_edit.html' ,data)
    
