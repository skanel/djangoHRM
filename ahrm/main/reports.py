#####################################################################
# Project:    A*HRM
# Title:     Reports:output PDF files dynamically using Django reports 
# Version:     0001
# Last-Modified:     2009-02-26 05:36:39  (Thu, 26 April 2009)        
# Author:     Sokha, Sin , Sanya, Mesa , Kanel (ALLWEB DEVELOPERS) 
# Status:     Active
# Type:     Process
# Created:     03-April-2009
# Post-History:     20-April-2009
######################################################################
from ahrm.main.models import Employee,Experience,Education,Skill, Company
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import Context
from django.conf import settings
import StringIO
import ho.pisa as pisa
import datetime
import time,os
import Image
import cgi
import csv


date_str = datetime.datetime.now() 
today = date_str.strftime("%Y-%m-%d:%H:%M")
#@login_required
def employee_report(request, id):
    '''
      Function: employee_report
       ----------------------------    
        request: the value of HTTP request
             id: the value of employee id
             
        returns: report employee to PDF by specific id 
    ''' 
    get_employee = get_object_or_404(Employee, id=id)
    fullname = get_employee.lname + get_employee.fname.upper()    

    if get_employee.active != False:
         status = 'working'
    else:
         status = 'terminated'
    def employee_age(): 
        current_year = time.localtime()
        year = get_employee.birthday.timetuple()
        age = current_year[0] - year[0]
        return age

    #@login_required
    def ouputting_pdf(template_src, context_dict):
         
        template = get_template(template_src)
        context = Context(context_dict)
        html  = template.render(context)   
        html = html.encode('UTF-8')     
        reportCSS = open(settings.MEDIA_ROOT+"/css/reports.css","r").read() 
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(html), result, path=os.path.abspath(template_src), default_css=reportCSS, encoding="utf-8")
        if not pdf.err:
            response = HttpResponse(result.getvalue(),mimetype='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=%s_%s.pdf' % (fullname,today)
            return response
            
            return HttpResponse('Create  your pdf! %s' % cgi.escape(html))    
           
    return ouputting_pdf('reports/employee_report_pdf.html',{
                         'pagesize':'A4',
                         'curr_employee':get_employee,
                         'status':status,
                         'url':'../'+settings.MEDIA_ROOT})


@login_required
def outputting_csv(request, id):
    '''
       Function: ouput_csv
       ----------------------------    
        request: the value of HTTP request
             id: the value of employee id
             
        returns: report employee to CSV by specific id 
    ''' 
    # Create CSV file name
    get_employee = get_object_or_404(Employee, id=id)    
    fullname = get_employee.lname + get_employee.fname.upper()
    response = HttpResponse(mimetype='text/csv')    
    response['Content-Disposition'] = 'attachment; filename=%s_%s.csv' % (fullname,today)
    # Write headers to CSV file
    writer = csv.writer(response)    
    cell_headers = ['Birthday', 'Marital status', 'Driver licence', 'Street', 'City','zip code','Phone','Mail','Date joined']    
    writer.writerow(cell_headers)
    # Write data to CSV file
    template = get_template('employees/employee_report_csv.txt')
    c = Context({
        'get_employee': get_employee,
    })
    response.write(template.render(c))
    # Return CSV file to browser as download
    return response


@login_required
def contacts_list(request):
    sess = request.session['AHRM_SESSION']
    com_id = sess.company_id
    com = Company.objects.get(id = com_id)

    employees = Employee.objects.filter(company = com_id, active = True).order_by('fname', 'lname')
    
    #@login_required
    def ouputting_pdf(template_src, context_dict):
         
        template = get_template(template_src)
        context = Context(context_dict)
        html  = template.render(context)        
        #print html
        reportCSS = open(settings.MEDIA_ROOT+"/css/contacts_list_reports.css","r").read() 
        result = StringIO.StringIO()
        #pdf = pisa.pisaDocument(StringIO.StringIO(html).encode("UTF-8"), result, path=os.path.abspath(template_src), default_css=reportCSS )
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode('UTF-8')), result, path=os.path.abspath(template_src), default_css=reportCSS, encoding="utf-8")
        if not pdf.err:
            response = HttpResponse(result.getvalue(),mimetype='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=contacts_list.pdf'
            return response
            
            return HttpResponse('Create  your pdf! %s' % cgi.escape(html))    
           
    return ouputting_pdf('reports/employees_contacts_list.html',{
                         'pagesize':'A4',
                         'employees':employees,
                         'company': com,
                         'url':'../'+settings.MEDIA_ROOT})
