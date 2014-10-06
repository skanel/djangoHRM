#####################################################################
# Project:    A*HRM
# Title:     Position controller 
# Version:     0001
# Last-Modified:     2009-02-26 05:36:39  (Thu, 26 April 2009)        
# Author:     Sokha, Sin , Sanya, Mesa , Kanel (ALLWEB DEVELOPERS) 
# Status:     Active
# Type:     Process
# Created:     03-April-2009
# Post-History:     20-April-2009
######################################################################
from libs import *

@login_required
def positions_list(request):
    data = initialize_view(request)
    data['positions'] = Position.objects.filter(company=data['company_id'])
    return render_to_response('positions/positions_list.html', data)

@login_required
def position_detail(request):
    return position_save_all(request, 0)
    data = initialize_view(request)
    form = PositionForm()
    data['position'] = form
    return render_to_response('positions/position_edit.html', data)

def position_save(request):
    pos_id = 0
    if request.POST.has_key('pos_id') :
        pos_id = int(request.POST['pos_id'])
    return position_save_all(request, pos_id)

def position_edit(request, pos_id):
    return position_save_all(request, pos_id)

@login_required
def position_save_all(request, pos_id):
    data = initialize_view(request)
    if (request.method == "POST" and request.POST.has_key('btn_save')):
        if pos_id != 0 :
            position = Position.objects.get(id=pos_id)
            form = PositionForm(request.POST, instance=position)
        else :
            position = Position()
            com = Company.objects.get(id=data['company_id'])
            position.company = com
            print com
            form = PositionForm(request.POST,instance=position)
        if (form.is_valid()) :
            form.save()
            return HttpResponsePermanentRedirect("/position")
        else :
            data['pos_id'] = pos_id
    else :
        if pos_id != 0 :
            position = Position.objects.get(id=pos_id)
            form = PositionForm(instance=position)
            data['pos_id'] = pos_id
        else  :
            form = PositionForm()
    
    data['position'] = form
    return render_to_response('positions/position_edit.html', data)

@login_required
def position_delete(request, pos_id):
    data = initialize_view(request)
    pos = Position.objects.get(id=pos_id)
    pos.delete()
    return HttpResponsePermanentRedirect("/position")    
