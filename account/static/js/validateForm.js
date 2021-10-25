// Validate Form using FormValidation

$.validator.addMethod('laxEmail', function (value, elements) {
    return value.search(/^\w+@[a-zA-Z_]+?\.[a-zA-Z]{1}$/)
}, 'Type valid Email!!');

$.validator.addMethod('passwordCheck', function (value, elements) {
    return value.search(/[a-z]/) >= 0 && value.search(/[A-Z]/) >= 0
        && value.search(/[0-9]/) >= 0 && value.search(/[^\w\s]/) >= 0
}, 'should contain at-least one Lower-Case Character + at-least one Upper-Case Character + at-least one Numer + at-least one Special Character ');

$.validator.addMethod('usenameCheck', function (value, elements) {
    return value.search(/^[\w\s]+$/i) == 0
}, 'should contain only Lower-Case, Upper-Case Characters & Numbers');

$(document).ready( function () {
    $("#regForm").validate( {
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
            contactno: {
                required: true,
                minlength: 10,
                maxlength: 10,
                number: true
            },
            username: {
                required: true,
                minlength: 4,
                usenameCheck: true
            },
            password: {
                required: true,
                minlength: 8,
                passwordCheck: true
            }
        },
        messages: {
            fname: {
                required: 'Please enter your First Name',
                minlength: 'First Name must contain at-least 2 characters'
            },
            lname: {
                required: 'Please enter your Last Name',
                minlength: 'Last Name must contain at-least 2 characters'
            },
            email: {
                required: 'Please enter your Email ID',
            },
            contactno: {
                required: 'Please enter Contact Number',
                minlength: 'Contact Number must be at-least 10 digit long',
                maxlength: 'Contact Number must be at-least 10 digit long',
                number: 'Enter Number only, no characters are allowed'
            },
            username: {
                required: 'Please type your Username',
                minlength: 'Username must contain at-least 4 characters'
            },
            password: {
                required: 'Please type your password',
                minlength: 'Password must be at-least 8 characters long'
            }
        },
        errorElement: 'em',
        errorPlacement: function ( error, element ) {
            //Add the 'help-block' class to the error element
            error.addClass("help-block");
            if(element.prop( "type" )  == "text" ) {
                error.insertAfter(element.parent("label"));
            }else {
                error.insertAfter(element);
            }
            if (element.prop("type") == "email") {
                error.insertAfter(element.parent("label"));
            } else {
                error.insertAfter(element);
            }
        },
        highlight: function (element, errorClass, validClass) {
            $(element).parents(".err").addClass("has-error").removeClass("has-success");
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element).parents(".err").addClass("has-success").removeClass("has-error");
        }
    });
});




// Show - Hide Password - Registration Form

(function () {

    var PasswordToggler = function (element, field) {
        this.element = element;
        this.field = field;

        this.toggle();
    };

    PasswordToggler.prototype = {
        toggle: function () {
            var self = this;
            self.element.addEventListener("change", function () {
                if (self.element.checked) {
                    self.field.setAttribute("type", "text");
                } else {
                    self.field.setAttribute("type", "password");
                }
            }, false);
        }
    };

    document.addEventListener("DOMContentLoaded", function () {
        var checkbox = document.querySelector("#showPass"),
            pwd = document.querySelector("#pwd"),
            form = document.querySelector("#regForm");



        var toggler = new PasswordToggler(checkbox, pwd);

    });

})();


// Show - Hide Password - Login Form

(function () {

    var PasswordToggler = function (element, field) {
        this.element = element;
        this.field = field;

        this.toggle();
    };

    PasswordToggler.prototype = {
        toggle: function () {
            var self = this;
            self.element.addEventListener("change", function () {
                if (self.element.checked) {
                    self.field.setAttribute("type", "text");
                } else {
                    self.field.setAttribute("type", "password");
                }
            }, false);
        }
    };

    document.addEventListener("DOMContentLoaded", function () {
        var checkbox = document.querySelector("#showPass"),
            pwd = document.querySelector("#pwd"),
            form = document.querySelector("#loginForm");



        var toggler = new PasswordToggler(checkbox, pwd);

    });

})();
