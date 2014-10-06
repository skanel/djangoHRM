#####################################################################
# Project:    A*HRM
# Title:     Company controller 
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
from django.utils.translation import ugettext

@login_required
def company_inititialize(request):
    #data = initialize_view(request)
    return company_save(request, -1)
    

''' after login and then enter a company '''
@login_required
def enter_company(request, com_id):
    com = Company.objects.get(id=com_id)
    try:
        ses =  request.session['AHRM_SESSION']
    except KeyError:
        ses = AHRMSession()
    ses.company_name = com.name
    ses.company_id = com.id
    request.session['AHRM_SESSION'] = ses 
    return HttpResponsePermanentRedirect("/mainpage")

''' Change a company '''
@login_required
def change_company(request):
    ses = request.session['AHRM_SESSION']
    ses.company_name = ''
    ses.company_id = 0 
    request.session['AHRM_SESSION'] = ses
    return HttpResponsePermanentRedirect("/companies/show")


''' Edit a company '''
def company_edit(request, com_id):
    return company_save(request, com_id)

'''  Company creation '''
def company_new(request):
    return company_save(request, 0)

''' Saving company, this will be called by functions company_edit or company_new '''
@login_required
def company_save(request, com_id):
    data = initialize_view(request)
    if request.method == 'POST' and request.POST.has_key('com_edit_save'):
        # this is the saving process
        if com_id != 0 and com_id != -1 : 
            com = Company.objects.get(id=request.POST['com_id'])
            form = forms.CompanyForm (request.POST, request.FILES, instance=com)
        else:
            com_name = request.POST['id_name']
            if com_name == '' :
                data['error_name'] = 'error'
            com = Company(name=com_name)
            form = forms.CompanyForm (request.POST, request.FILES, instance=com)
            
        if form.is_valid() and com.name != '':
            if com.logo and request.FILES:
                os.remove(com.logo.path)
            if com.banner and request.FILES:
                os.remove(com.banner.path)
            form.save()
            if com_id == -1 :
                return HttpResponseRedirect('/companies/show')
            else :
                return HttpResponseRedirect('/companies/list')
        else :
            data['com_name'] = com.name
            data['company_logo'] = com.logo
            data['com_id'] = com.id
    else:
        # this is the initialization of interface
        if com_id != 0 and com_id != -1: 
            com = Company.objects.get(id=com_id)
            form = forms.CompanyForm (instance=com)
            data['com_name'] = com.name
            data['company_logo'] = com.logo
            data['com_id'] = com_id
        else :
            form = forms.CompanyForm ()
    
    if com_id == -1 :
        data['initialize'] = True
    data['form'] = form
    
    return render_to_response('companies/company_edit.html', data)

''' delete a company '''
@login_required
def company_delete(request, com_id):
    data = initialize_view(request)
    com = Company.objects.get(id=com_id)
    com.delete()
    return HttpResponseRedirect('/companies/list')
@login_required
def company_structure(request):
    ses = request.session['AHRM_SESSION']
    data = initialize_view(request)   
    data['id'] = ses.company_id
    data['name'] = ses.company_name
    return render_to_response('companystructure.html', data)


"function use to generate json data for tree"
@login_required
def treedata(request,id):
    strdata ='['   
    def def_depfather(id,compID):
        objComp = Company.objects.get(id=compID)
        if id == None:
            objDepList = Department.objects.filter(department_father = None,company = objComp).order_by('order_id')
        else :
            obj = Department.objects.get(id=id)
            objDepList = Department.objects.filter(department_father = obj,company = objComp).order_by('order_id')
        if len(objDepList) == 0 :
            json_obj = '{"text":' + '"' + obj.name + '",' + '"id":' + '"department@@@' + str(obj.id) + '",' + '"cls":"file","leaf":"true"'                         
            return json_obj
        else:
            if id != None:                
                json_obj = '{"text":' + '"' + obj.name + '",' + '"id":' + '"department@@@' + str(obj.id) + '",' + '"cls":"folder","children":['
            else :
                json_obj = ''            
            for objDep in objDepList:
                json_obj += def_depfather(objDep.id,compID)
                json_obj += '},'
            json_obj = json_obj[0:-1]
            json_obj += ']'                
            return json_obj    
    strdata += def_depfather(None,id)   
    template = loader.get_template("treedata.html")    
    jsonData = Context({                         
                         'jsondata' : strdata,                         
                         })
    sendjson = template.render(jsonData)
    return HttpResponse(sendjson)          
        
    
"function use to view data every click on tree element"
@login_required
def viewdetail(request):      
    template = loader.get_template("treedata.html")
    objType = request.POST.get("objType")
    objId = request.POST.get("objId")
    if objType == 'company':
        objType = 'Company'
        comp = Company.objects.get(id=objId)
        name = comp.name
        desc = comp.desc
        id = comp.id
        btEdit = ''
        btDelete = ''       
    else : 
        if objType == 'department':
            objType = 'Department'
            dept = Department.objects.get(id=objId)
            name = dept.name
            desc = dept.desc
            id = dept.id    
            btEdit = '<input type="submit" value="' + ugettext('Edit Department') + '" name="dep_edit"/>'
            btDelete ='<input type="submit" value="' + ugettext('Delete Department') + '" name="dep_delete" onclick="return beforeDelete();"/>'
              
    htmlstring = '<form id="form1" name="form1" method="post" action="/department/add/">' 
    htmlstring += '<table border="0"><tr><td width="160"><b>'+ ugettext(objType +' name') + '</b></td><td width="372">:'+ name +'</td></tr>'
    htmlstring += '<tr><td valign="top"><b>' + ugettext('Description') + '</b></td><td>:<label>'+desc+'</label></td></tr>'    
    htmlstring += '<tr><td align="right"><input type="submit" value="' + ugettext('Add Department') + '" name="dep_add"/></td><td >'+btEdit+'&nbsp;'+btDelete+'</td></tr>'
    htmlstring += '<tr><td><input type="hidden" value="' + objType + '" name="type" /></td><td ></td></tr>'
    htmlstring += '<tr><td><input type="hidden" value="'+ str(id) +'" name="id"/></td><td ></td></tr></table></form>'    
    jsonData = Context({                         
                         'jsondata' : htmlstring,                         
                         })             
    sendjson = template.render(jsonData)     
    return HttpResponse(sendjson)

''' Show list of companies from login page '''
def companies_show(request):
    return companies_show_list(request, 0)

''' Show list of companies in order to edit '''
def companies_list(request):
    return companies_show_list(request, 1)

''' this function will be called by  companies_show and companies_list function'''
@login_required
def companies_show_list(request, process):
    data = initialize_view(request)
    user = request.user
    user_group = user.groups.all()
    is_hr = 0 
    is_manager = 0
    try :
        if len(user_group)>0 and user_group[0].name == 'HR' :
            is_hr = 1
        elif len(user_group)>0 and user_group[0].name == 'Manager' :
            is_manager = 1
    except KeyError:
        pass
    
    com_list = []
    if is_hr == 1 or is_manager == 1:
        user_com_list = UserCompany.objects.filter(user=user.id).order_by('company')
        for user_com in user_com_list:
            com_list.append(Company.objects.get(id=user_com.company_id));
    else :
        com_list = Company.objects.all().order_by('id')
            
    try:
        ses =  request.session['AHRM_SESSION']
        ses.multi_companies = 1
        request.session['AHRM_SESSION'] = ses
    except KeyError:
        ses = AHRMSession()
        ses.multi_companies = 1
        ses.user_type = is_hr
        request.session['AHRM_SESSION'] = ses
    
    data['com_id']=ses.company_id
    data['multi_companies'] = ses.multi_companies
    data['company_list'] = com_list
    data['user_type'] = ses.user_type
    data['process'] = process
    
    if is_hr == 0 and len(com_list) == 0:
        return HttpResponsePermanentRedirect("/company/initialize")
    t = loader.get_template('companies/companies_show_list.html')
    c = Context(data)
    return HttpResponse(t.render(c))

def movenode(request):
    depOldType = request.POST.get("depOldType")
    depOldId = request.POST.get("depOldId")
    depNewType = request.POST.get("depNewType")
    depNewId = request.POST.get("depNewId")
    depNodeId = request.POST.get("depNodeId")
    index = request.POST.get("number")
    
#    print depOldType
#    print depOldId 
#    print depNewType
#    print depNewId 
#    print depNodeId
#    print index
    
    objDepartment = Department.objects.get(id = depNodeId)
    if depNewType == "company":
        objNewDepartment = None
    elif depNewType == "department":
        objNewDepartment = Department.objects.get(id=depNewId)
    objDepartment.department_father = objNewDepartment  
    objTmpDep = Department.objects.filter(department_father = objNewDepartment).order_by('order_id')    
    if len(objTmpDep) == 0 :                
        objDepartment.order_id = 1
    elif len(objTmpDep) > 0 :        
        count = 1        
        for i in range(0,len(objTmpDep)):             
            if depNewId != depOldId :          
                if int(index) == count :
                    objDepartment.order_id = objTmpDep[i].order_id + 1            
                elif int(index) < count:
                    if int(index) == 0:                        
                        objDepartment.order_id = 1
                    objTmpDep[i].order_id += 1
                    tempDepartment = Department()
                    tempDepartment = objTmpDep[i]
                    tempDepartment.save()
            else :
                if int(depNodeId) == objTmpDep[i].id  :
                    continue  
                else:
                    if int(index) == count:
                        objDepartment.order_id = objTmpDep[i].order_id + 1      
                    elif int(index) < count:
                        if int(index) == 0 :                            
                            objDepartment.order_id = 1
                        objTmpDep[i].order_id += 1
                        tempDepartment = Department()
                        tempDepartment = objTmpDep[i]
                        tempDepartment.save()
                    
            count = count + 1
    objDepartment.save()    
    
    # reorder department
    
    objNewDep = Department.objects.filter(department_father = objNewDepartment).order_by('order_id')
    for i in range(0,len(objNewDep)):
        objNewDep[i].order_id = i + 1
        tempDepartment = Department()
        tempDepartment = objNewDep[i]
        tempDepartment.save()
    
         
    
    strdata = ""
    template = loader.get_template("treedata.html")    
    jsonData = Context({                         
                         'jsondata' : strdata,                         
                         })
    sendjson = template.render(jsonData)
    return HttpResponse(sendjson) 