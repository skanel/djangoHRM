#####################################################################
# Project:    A*HRM
# Title:     Helper controller 
# Version:     0001
# Last-Modified:     2009-02-26 05:36:39  (Thu, 26 April 2009)        
# Author:     Sokha, Sin , Sanya, Mesa , Kanel (ALLWEB DEVELOPERS) 
# Status:     Active
# Type:     Process
# Created:     03-April-2009
# Post-History:     20-April-2009
######################################################################
class AHRMSession :
    company_id = 0
    company_name = ''
    multi_companies = 0
    user_type = 0
    user_id = 0


class UserCompanyRegister :
    company_id = 0
    company_name = ''
    company_desc = ''
    register = False
    
class Tabs :
    def __init__(self):
        self.tab_elements = {}
        self.tab_item_order = []
    def add_element(self, tab_element):
        self.tab_elements[tab_element.tab_name] = tab_element
        self.tab_item_order.append(tab_element.tab_name)
    
class TabElement :
    def __init__(self, tab_name, tab_label, tab_link, tab_template):
        self.tab_name = tab_name
        self.tab_label = tab_label
        self.tab_link = tab_link
        self.tab_template = tab_template

        