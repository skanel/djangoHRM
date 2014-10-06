/*
 * Ext JS Library 2.2
 * Copyright(c) 2006-2008, Ext JS, LLC.
 * licensing@extjs.com
 * 
 * http://extjs.com/license
 */

Ext.onReady(function(){
    var win;
    var button;
    if (Ext.get('show-btn') != null) {
        button = Ext.get('show-btn');
        button.on('click', function(){
        // create the window on the first click and reuse on subsequent clicks
        if(!win){
            win = new Ext.Window({
                title   : 'About AHRM',
                applyTo     : 'about_ahrm',
                layout      : 'fit',
                width       : 650,
                closeAction :'hide',
                height      : 450,
                resizable   : false, 
                plain       : false,
                items       : new Ext.Panel({
                    rederTo        : 'about_ahrm_data',
                    autoLoad : '/about_ahrm',
                    html : Ext.about.ahrm,
                    scripts: true,
                    autoScroll  : true
                    
                }),

                buttons: [{
                    text     : 'Close',
                    handler  : function(){
                        win.hide();
                    }
                }]
            });
	        }
	        win.show(button);
	    });
    }

    
});