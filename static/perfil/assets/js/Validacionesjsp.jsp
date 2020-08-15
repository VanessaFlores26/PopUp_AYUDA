<%-- 
    Document   : Validacionesjsp
    Created on : 04-08-2020, 08:03:13 PM
    Author     : Alexia
--%>

<link href="statics/perfil/assets/css/bulma.css" rel="stylesheet" type="text/css" />


$.validator.setDefaults({
submitHandler: function() {
alert("submitted!");
}
});

$().ready(function(){
//jquery
//
$("#myform").validate({
rules:{
name:{
required: true
}



},
messages:{
name: {
required: "Complete el campo"
}


}
});
});