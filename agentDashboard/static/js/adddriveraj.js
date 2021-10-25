//======================================================================================
//Validate Add Car Form Data

$.validator.addMethod('laxEmail', function (value, elements) {
    return value.search(/^\w+@[a-zA-Z_]+?\.[a-zA-Z]{1}$/)
}, 'Type valid Email!!');

$(document).ready(function () {
    console.log("jQuery Validation");
    $(".addDriver").validate({
        rules: {
            fname: {
                required: true,
                minlength: 2
            },
            lname: {
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
            lcNumber: {
                required: true
            },
            lcExp: {
                required: true
            }
        },

        submitHandler: function () {

            console.log("Ajax Function is called!!!");
            // event.preventDefault()

            var formData = new FormData();



            formData.append('fname', $('#fname').val());
            formData.append('lname', $('#lname').val());
            formData.append('email', $('#email').val());
            formData.append('cno', $('#cno').val());
            formData.append('lcNumber', $('#lcNumber').val());
            formData.append('lcExp', $('#lcExp').val());
            formData.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());

            $.ajax({
                type: 'POST',
                url: 'adddriver',
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                enctype: 'multipart/form-data',
                success: function () {
                    swal({
                        text: 'Driver Details has been added successfully!',
                        icon: 'success',
                        closeOnClickOutside: true,
                        closeOnEsc: true,
                    });
                    $(".addDriver").trigger('reset');
                    $("#fname").focus();
                    return false;
                },
                error: function (xhr, errmsg, err) {
                    console.log(xhr.status + ":" + xhr.responseText);
                    swal({
                        text: 'Car Details not added successfully!',
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
            fname: {
                required: 'Please enter First Name',
                minlength: 'First Name must contain at-least 2 characters'
            },
            lname: {
                required: 'Please enter Last Name',
                minlength: 'Last Name must contain at-least 2 characters'
            },
            email: {
                required: 'Please enter your Email ID',
            },
            cno: {
                required: 'Please enter your Contact Number',
                minlength: 'Contact Number must contain 10 digits only',
                maxlength: 'Contact Number must contain 10 digits only',
                number: 'Enter Number only, no characters are allowed'
            },
            lcNumber: {
                required: 'Please enter Driving License Number',
            },
            lcExp: {
                required: 'Please enter Driving License Expiry Date',
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
