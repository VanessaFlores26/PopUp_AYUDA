// Wait for the DOM to be ready

$(function () {
    // Initialize form validation on the registration form.
    // It has the name attribute "registration"
    $("form[name='modificar']").validate({
        // Specify validation rules
        rules: {
            nombre: "required",
            email: {
                required: true,
                email: true
            },
            pais: "required",
            ciudad: "required",
            biografia: "required",

            telefono:
            {
                required: true,
                minlength: 8
            },
            messages:
            {
                nombre: "*Por favor, ingrese sus nombres",
                email: "*Por favor, ingrese su email",
                pais: "*Por favor, ingrese su pais",
                ciudad: "*Por favor, ingrese su ciudad",
                biografia: "*Por favor, escriba su biografía",
            },

            telefono:
            {
                required: "*Por favor, ingrese su telefono",
                minlength: "*Su nombre de usuario debe contener al menos 8 d�gitos"
            },
        }
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function (form) {
            form.submit();
        }

    })

});


