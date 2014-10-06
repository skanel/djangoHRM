#####################################################################
# Project:    A*HRM
# Title:     Main Page controller 
# Version:     0001
# Last-Modified:     2009-02-26 05:36:39  (Thu, 26 April 2009)        
# Author:     Sokha, Sin , Sanya, Mesa , Kanel (ALLWEB DEVELOPERS) 
# Status:     Active
# Type:     Process
# Created:     03-April-2009
# Post-History:     20-April-2009
######################################################################
from libs import *
from django.conf import settings
from django.utils import translation



''' This is the index which redirect to the login page'''
def index(request):
    data = initialize_view(request)
    if request.session.has_key('AHRM_SESSION'):
        del request.session['AHRM_SESSION']
    t = loader.get_template('login_template.html')
    c = Context(data)
    return HttpResponse(t.render(c))

@login_required
def goto_mainpage(request):
    data = initialize_view(request)
    ses = request.session['AHRM_SESSION']
    com_id = ses.company_id
    company = Company.objects.get(id = com_id)
    data['company'] = company
    c = Context(data)
    t = loader.get_template('main_page.html')
    return HttpResponse(t.render(c))

@login_required
def help(request):
    return render_to_response('help.html')

@login_required
def about_ahrm(request):
    return render_to_response('about_ahrm.html')

