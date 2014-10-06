#####################################################################
# Project:    A*HRM
# Title:     User controller 
# Version:     0001
# Last-Modified:     2009-02-26 05:36:39  (Thu, 26 April 2009)        
# Author:     Sokha, Sin , Sanya, Mesa , Kanel (ALLWEB DEVELOPERS) 
# Status:     Active
# Type:     Process
# Created:     03-April-2009
# Post-History:     20-April-2009
######################################################################
from libs import *
from string import replace
from django.utils.translation import ugettext_lazy

def control_login(request):
    return HttpResponsePermanentRedirect("/")

''' Authentication '''
def submit_login(request):   
    if request.method != 'POST' or (not request.POST.has_key('user_name')) :
        return HttpResponsePermanentRedirect("/")
    username = request.POST['user_name']
    password = request.POST['user_pwd']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            #Save user object to session
            login(request, user)
            is_hr = -1
            is_manager = -1
            user_group = user.groups.all()
            try :
                if len(user_group)>0 : 
                   if user_group[0].name == 'HR' :
                       is_hr = 1
                       is_manager = 0
                   elif user_group[0].name == 'admin' :
                       is_hr = 0
                       is_manager = 0
                   elif user_group[0].name == 'Manager' :
                       is_hr = 0
                       is_manager = 1
                   else :
                       is_hr = -1
                       is_manager = -1
                else :
                   is_hr = -1
                   is_manager = -1
            except KeyError:
                pass
            if user.is_superuser :
                is_hr = 0
            userCompany = UserCompany.objects.filter(user=user.id)
            if len(userCompany) == 1 and is_hr == 1 :
                ses = AHRMSession()
                com = userCompany[0].company
                ses.company_id = com.id 
                ses.company_name = com.name
                ses.multi_companies = 0
                ses.user_type = 1
                ses.user_id = user.id
                request.session['AHRM_SESSION'] = ses
                return HttpResponsePermanentRedirect("/mainpage")
            elif is_manager == 1 :
                ses = AHRMSession()
                ses.multi_companies = 1
                ses.user_type = 2
                ses.user_id = user.id
                request.session['AHRM_SESSION'] = ses
                return HttpResponsePermanentRedirect("/companies/show")
            elif is_hr in (0, 1):
                return HttpResponsePermanentRedirect("/companies/show")
            else :
                t = loader.get_template('login_template.html')
                c = Context({'login_failed' : "Unknown user type of this user", 'user_name' : username, 'LANGUAGES':settings.LANGUAGES})
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            t = loader.get_template('login_template.html')
            c = Context({'login_failed' : ugettext_lazy("This user is disabled."), 'user_name' : username, 'LANGUAGES':settings.LANGUAGES})
    else:
        t = loader.get_template('login_template.html')
        c = Context({'login_failed' : ugettext_lazy("User or Password invalid."), 'user_name' : username, 'LANGUAGES':settings.LANGUAGES})
        
    
    return HttpResponse(t.render(c))


''' Logout function '''
def user_logout(request):
    try:
        del request.session['AHRM_SESSION']
    except KeyError:
        pass
    # unregister user from session
    logout(request)
    return HttpResponsePermanentRedirect("/")

''' Goto Main Page '''

@login_required
def users_list(request):
    data = initialize_view(request)
    users = User.objects.all()
    if data['user_type'] == 2:
        usersCompany = UserCompany.objects.filter(company=data['company_id'])
        list = []
        for u in usersCompany:
           list.append(u.user_id)
        users = users.filter(id__in = list)
        
    data['users'] = users 
    user_groups = {}
    for user in users :
        groups = user.groups.all()
        if len(groups) > 0 :
            group_name = user.groups.all()[0].name
        else :
            group_name = ''
        
        user_groups[user.username] = group_name
        
    data['user_groups'] = user_groups 
    t = loader.get_template('users/users_list.html')
    c = Context(data)
    return HttpResponse(t.render(c))

@login_required
def user_edit(request, user_id):
    data = initialize_view(request)
    user = User.objects.get(id=user_id)
    coms = Company.objects.all()
    user_group = Group.objects.filter(user=user_id)
    group_id = 0
    if user_group:
        group_id = user_group[0].id
    
    if data['user_type'] == 2:
        usersCompany = UserCompany.objects.filter(user=data['user_id'])
        if len(usersCompany) > 1:
            list = []
            for u in usersCompany:
               list.append(u.company_id)
            coms = coms.filter(id__in = list)
        else:
            coms = coms.filter(id = usersCompany[0].company_id)
    
    if request.method == 'POST' and request.POST.has_key('btn_save'): 
        group_id = request.POST.get('groups')
        user.groups = group_id
        form = UserForm(request.POST, instance=user)
        if form.is_valid() :
            form.save()
            for com in coms:
                if request.POST.has_key('main_check_' + str(com.id)) :
                    user_coms = UserCompany.objects.filter(company=com.id, user=user.id)
                    if len(user_coms) == 0 :
                        user_com = UserCompany()
                        user_com.user = user
                        user_com.company = com
                        user_com.save()
                else :
                    user_coms = UserCompany.objects.filter(company=com.id, user=user.id)
                    if len(user_coms) == 1 :
                        user_coms[0].delete()                    
    else :
        form = UserForm(instance=user)
         
#    form = UserCreationForm()
    
    data['form'] = form
    data['user_id'] = user.id
    data['user_name'] = user.username
    data['group_id'] = group_id
    user_com_reg_list = []
    #user_company = UserCompany.objects.all()
    for com in coms :
        user_com_reg = UserCompanyRegister()
        user_com_reg.company_id = com.id
        user_com_reg.company_name = com.name
        user_com_reg.company_desc = com.desc
        user_com_reg.register = False
        
        res = UserCompany.objects.filter(company=com.id, user=user.id)
        #res = res.filter(user=user.id)
        if len(res) > 0 :
            user_com_reg.register = True
        user_com_reg_list.append(user_com_reg)
    data['coms'] = user_com_reg_list
    t = loader.get_template('users/user_edit.html')
    c = Context(data)
    return HttpResponse(t.render(c))

@login_required
def user_create(request):
    data = initialize_view(request)
    if request.method == 'POST' and request.POST.has_key('btn_save'):
        form = UserCreationForm(request.POST)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect('/users/list');
    else :
        form = UserCreationForm()
    #form = UserCreationForm()
    data['form'] = form
    t = loader.get_template('users/user_create.html')
    c = Context(data)
    return HttpResponse(t.render(c))

@login_required
def user_update_pwd(request, user_id):
    data = initialize_view(request)
    user = User.objects.get(id=user_id)
    if request.method == 'POST' and request.POST.has_key('btn_set_pwd_save'):
        pwd1 = request.POST['new_password1']
        pwd2 = request.POST['new_password2']
        val = {'new_password1' : pwd1, 'new_password2' :pwd2}
        form = SetPasswordForm(user, val)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect('/user/detail/' + user_id)
    else :
        form = SetPasswordForm(user)
    data['form'] = form
    data['user_id'] = user.id
    data['user_name'] = user.username
    t = loader.get_template('users/user_set_password.html')
    c = Context(data)
    return HttpResponse(t.render(c))

@login_required
def user_delete(request,user_id):
    user =User.objects.get(id=user_id)
    user.delete()
    return HttpResponseRedirect('/users/list')

''' Change a password of a user '''
@login_required
def change_password(request):
    data = initialize_view(request)
    try:
        btn = request.POST['btn_chg_pwd']
        form = PasswordChangeForm(request.POST)
        user = request.user
        old_password = request.POST['old_password']
        if user.check_password(old_password) :
            new_password1 = request.POST['new_password1']
            new_password2 = request.POST['new_password2']
            if new_password1 == new_password2 :
                user.set_password(new_password1)
                user.save()
                return HttpResponsePermanentRedirect("/mainpage")
            else :
                data['error_message'] = ugettext_lazy('Confirm password is not correct.')
        else :
            data['error_message'] = ugettext_lazy('Your old password is not correct.')
        

    except KeyError:
        form = PasswordChangeForm(request.POST)

    data['a_form'] = form
    t = loader.get_template('users/change_pwd.html')
    c = Context(data)
    
    return HttpResponse(t.render(c))
        