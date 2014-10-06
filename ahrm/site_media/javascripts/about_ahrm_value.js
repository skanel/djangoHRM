/*
 * Ext JS Library 2.2
 * Copyright(c) 2006-2008, Ext JS, LLC.
 * licensing@extjs.com
 * 
 * http://extjs.com/license
 */

Ext.about = function(){
    var msgCt;

   
    return {
        msg : function(title, format){
            if(!msgCt){
                msgCt = Ext.DomHelper.insertFirst(document.body, {id:'msg-div'}, true);
            }
            msgCt.alignTo(document, 't-t');
            var s = String.format.apply(String, Array.prototype.slice.call(arguments, 1));
            var m = Ext.DomHelper.append(msgCt, {html:createBox(title, s)}, true);
            m.slideIn('t').pause(1).ghost("t", {remove:true});
        },

        init : function(){
            var t = Ext.get('exttheme');
            if(!t){ // run locally?
                return;
            }
            var theme = Cookies.get('exttheme') || 'aero';
            if(theme){
                t.dom.value = theme;
                Ext.getBody().addClass('x-'+theme);
            }
            t.on('change', function(){
                Cookies.set('exttheme', t.getValue());
                setTimeout(function(){
                    window.location.reload();
                }, 250);
            });

            var lb = Ext.get('lib-bar');
            if(lb){
                lb.show();
            }
        }
    };
}();

Ext.about.ahrm = '<table width="100%">';
Ext.about.ahrm +=   '<tr>';
Ext.about.ahrm +=       '<td><img src="/site_media/images/allwelogo.png" width="150" height="150" alt="Human Resource Management" /></td>';
Ext.about.ahrm +=   '</tr>';
Ext.about.ahrm +=   '<tr>';
Ext.about.ahrm +=       '<td><font color="#E792A0"> <h2>AHRM</h2></font></td>';
Ext.about.ahrm +=   '</tr>';
Ext.about.ahrm +=   '<tr>';
Ext.about.ahrm +=   '<td><font color="gray"> Version 1.1</td>';
Ext.about.ahrm +=   '</tr>';
Ext.about.ahrm +=   '</table>';       
Ext.about.ahrm +=   '<br/>';
Ext.about.ahrm +=   '<table width="100%">';
Ext.about.ahrm +=       '<tr>';
Ext.about.ahrm +=           '<td>'; 
Ext.about.ahrm +=               '<p align="justify">';
Ext.about.ahrm +=                   'ALLWEB  Human Resource Management is a new system which was created by an open source developers team of ALLWEB  Company.'; 
Ext.about.ahrm +=                   'The goal of this system is to provide facilities of company,  department, and employee management'; 
Ext.about.ahrm +=                   'for every user at every level. We provide the functionality that support daily activities at'; 
Ext.about.ahrm +=                   'department of human resources.'; 
Ext.about.ahrm +=               '</p><br/>';
Ext.about.ahrm +=               '<p align="justify">';
Ext.about.ahrm +=                   'ALLWEB Human Resource Management is really suitable for small and mid-size business which its';  
Ext.about.ahrm +=                   'daily activities are not much complicated or sophisticated. However, we are  sure that it can'; 
Ext.about.ahrm +=                   'extend for giant business because of our well structure organization of this software.';
Ext.about.ahrm +=               '</p><br/>';
Ext.about.ahrm +=               '<p align="justify">';
Ext.about.ahrm +=                   'Created  by open source technologies, AHRM is the powerful software that is not only for end'; 
Ext.about.ahrm +=                   'user but also for other developers to add more functionalities for their  needs. Python with'; 
Ext.about.ahrm +=                   'Django framework are the main technologies that we decide to use to build this web system.'; 
Ext.about.ahrm +=               '</p>';
Ext.about.ahrm +=           '</td>';
Ext.about.ahrm +=       '</tr>';
Ext.about.ahrm +=   '</table>';
            
Ext.onReady(Ext.about.init, Ext.about);

