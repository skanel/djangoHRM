from django import template
from django.template import TemplateSyntaxError, Node, Context, Variable
from django.template.loader import get_template
from django.template.defaultfilters import stringfilter
from ahrm.main.helpers import Tabs, TabElement

from django.conf import settings

register = template.Library()

import re


@register.filter
@stringfilter
def make_department_links(str):
    def repl(m):
        return '<a href="/department/%s">%s</a>' % (m.group(2), m.group(1))
    return re.sub(">([\w ]+)\((\d+)\)", repl, str)


@register.filter
def tabs(parser, token):
    bits = token.contents.split()
    tabs = parser.compile_filter(bits[1])
    selected_tab = bits[2]
    return AHRMTabs(tabs, selected_tab)
tabs.safe = True

class AHRMTabs(Node):
    def __init__(self, tabs, selected_tab):
        self.tabs = tabs
        self.selected_tab = selected_tab
        if self.selected_tab[0] in ('"', "'") and self.selected_tab[0] == self.selected_tab[-1] :
            self.selected_tab_constance = True
            self.selected_tab = self.selected_tab[1:-1]
        else :
            self.selected_tab_constance = False
            self.selected_tab = Variable(self.selected_tab)
        #self.selected_tab = Variable(selected_tab)
        
    def render(self, context):
        tabs = self.tabs.resolve(context, True)
        selected_tab = self.selected_tab
        if self.selected_tab_constance == False:
            selected_tab = selected_tab.resolve(context)
        tab_elements = tabs.tab_elements
        have_selected = tab_elements.has_key(selected_tab)
        
        i = 0
        res = '<table cellspacing="0" cellpadding="0" margin="0" width="100%"><tr><td>'
        res = res + '<table border="0" cellspacing="0" cellpadding="0"><tr>'
        for k in tabs.tab_item_order:
            v = tab_elements[k]
            if (have_selected == False and i == 0) or (selected_tab == k):
                res = res + '<td class="ahrm_tab_selected" height="2">&nbsp;&nbsp;' + v.tab_label + '&nbsp;&nbsp;</td>'
                template_path = v.tab_template
            else :
                res = res + '<td class="ahrm_tab">&nbsp;&nbsp;<a href="' + v.tab_link +'">' + v.tab_label + '</a>&nbsp;&nbsp;</td>'
            i = i+1
        res = res + '</tr></table></td></tr><tr><td width="100%">'
        res = res + '<table class="ahrm_tab_content" width="98%"><tr><td width="2%">&nbsp;</td><td width="100%">'
        #print parser.compile_filter(self.tabs)
        
        try:
            t = get_template(template_path)
        except:
            if settings.TEMPLATE_DEBUG:
                raise
            t = None
        
        if t:
            res = res + t.render(context)
        res = res + '</td></tr></table></td></tr></table>' 
        return res

register.tag('tabs', tabs)