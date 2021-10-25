//Validate Contact us Form Data

$.validator.addMethod('laxEmail', function (value, elements) {
    return value.search(/^\w+@[a-zA-Z_]+?\.[a-zA-Z]{1}$/)
}, 'Type valid Email!!');


$(document).ready(function () {
    console.log("jQuery Validation");
    $(".contactUs").validate({
        rules: {
            name: {
                required: true,
                minlength: 2
            },
            email: {
                required: true,
                email: true,
                laxEmail: true
            },
            cno: {
                required: true,
                minlength: 10,
                maxlength: 10,
                number: true
            },
            sub: {
                required: true,
                maxlength: 50
            },
            msg: {
                required: true,
                maxlength: 250
            }
        },

        submitHandler: function () {

            console.log("Ajax Function is called!!!");
            // event.preventDefault()

            var formData = new FormData();

            formData.append('name', $('#name').val());
            formData.append('email', $('#email').val());
            formData.append('cno', $('#cno').val());
            formData.append('sub', $('#sub').val());
            formData.append('msg', $('#msg').val());
            formData.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());

            $.ajax({
                type: 'POST',
                url: 'contactus',
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                enctype: 'multipart/form-data',
                success: function () {
                    swal({
                        text: 'Thank You for Contacting Us, We will get back to you soon.',
                        icon: 'success',
                        closeOnClickOutside: true,
                        closeOnEsc: true,
                    });
                    $("#contactUs").trigger('reset');
                    return false;
                },
                error: function (xhr, errmsg, err) {
                    console.log(xhr.status + ":" + xhr.responseText);
                    swal({
                        text: 'Sorry, Something went wrong!!',
                        icon: 'error',
                        closeOnClickOutside: true,
                        closeOnEsc: true,
                    });
                    return false;
                }
            })

            return false;

        },

        messages: {
            name: {
                required: 'Please enter your Full Name',
                minlength: 'Name must contain at-least 2 characters'
            },
            email: {
                required: 'Please enter your Email ID',
            },
            cno: {
                required: 'Please enter Contact Number',
                minlength: 'Contact Number must be at-least 10 digit long',
                maxlength: 'Contact Number must be at-least 10 digit long',
                number: 'Enter Number only, no characters are allowed'
            },
            sub: {
                required: 'Please enter the Subject',
                maxlength: 'Subject should contain only 50 characters'
            },
            msg: {
                required: 'Please type in your query',
                maxlength: 'Your Message (Query) should contain only 250 characters'
            }
        },
        errorElement: 'em',
        errorPlacement: function (error, element) {
            //Add the 'help-block' class to the error element
            error.addClass("help-block");
            if (element.prop("type") == "text") {
                error.insertAfter(element.parent("label"));
            } else {
                error.insertAfter(element);
            }
            if (element.prop("type") == "checkbox") {
                error.insertAfter(element.parent("label"));
            } else {
                error.insertAfter(element);
            }
        },
        highlight: function (element, errorClass, validClass) {
            $(element).parents(".col-sm-5").addClass("has-error").removeClass("has-success");
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element).parents(".col-sm-5").addClass("has-success").removeClass("has-error");
        }
    });
});