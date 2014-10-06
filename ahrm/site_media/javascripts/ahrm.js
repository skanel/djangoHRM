function process(ahrm_action) {
    form_obj = document.forms[0];
    if (form_obj.name == "i18n_form") {
        form_obj = document.forms[1]; 
    }  
    form_obj.action = ahrm_action;
    form_obj.submit();
}

function openPopup(url) {
	//window.open(url,'popup','height=515,width=800,toolbar=no,status=no,scrollbars=yes,location=no,menubars=no,directories=no,resizable=no');
	
	//return false;
	
	 WindowObjectReference = window.open("/about_ahrm", "DescriptiveWindowName", "height=515,width=800,resizable=no,scrollbars=yes,status=yes");
	
    
}