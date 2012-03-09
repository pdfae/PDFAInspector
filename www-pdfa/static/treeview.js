function check_all(){
	var c = new Array();
 	c = document.getElementsByTagName('input');
 	for (var i = 0; i < c.length; i++){
 		if (c[i].type == 'checkbox'){
			c[i].checked = true;
		}
 	}
}
function uncheck_all(){
	var c = new Array();
 	c = document.getElementsByTagName('input');
 	for (var i = 0; i < c.length; i++){
 		if (c[i].type == 'checkbox'){
			c[i].checked = false;
		}
 	}
}