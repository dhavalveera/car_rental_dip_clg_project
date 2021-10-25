//======================================================================================
//Validate Add Car Form Data

$(document).ready( function () {
    console.log("jQuery Validation");
    $(".addCar").validate( {
        rules: {
            brandName: {
                required: true,
                minlength: 2
            },
            modelName: {
                required: true,
                minlength: 2
            },
            rcNumber: {
                required: true,
                minlength: 2
            },
            perKmsCost: {
                required: true,
                minlength: 2,
                number: true
            },
            features: 'required',
            transmission: 'required',
            fuelType: 'required',
            minKM: {
                required: true,
                number: true
            },
            priceAftrFreeKM: {
                required: true,
                number: true
            },
            seatcap: {
                required: true
            },
            carImg: {
                required: true,
                accept: "image/*"
            }
        },

        submitHandler: function() {

            console.log("Ajax Function is called!!!");
            // event.preventDefault()

            var formData = new FormData();

            //Checkbox Value
            var featuresjs = [];
            $.each($("input[name='features']:checked"), function () {
                featuresjs.push($(this).val());
            });

            formData.append('brandName', $('#brndName').val());
            formData.append('modelName', $('#mdlName').val());
            formData.append('rcNumber', $('#rcNo').val());
            formData.append('perKmsCost', $('#pkc').val());
            formData.append('feat', featuresjs);
            formData.append('transmission', $('#transmission').val());
            formData.append('fuelType', $('#fuelType').val());
            formData.append('minKM', $('#mink').val());
            formData.append('priceAftrFreeKM', $('#prcaftfrkm').val())
            formData.append('seatcap', $('#sc').val());
            formData.append('carImg', $('input[type=file]')[0].files[0]);
            formData.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());

            $.ajax({
                type: 'POST',
                url: 'addcar',
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                enctype: 'multipart/form-data',
                success: function () {
                    swal({
                        text: 'Car Details has been added successfully!',
                        icon: 'success',
                        closeOnClickOutside: true,
                        closeOnEsc: true,
                    });
                    $(".addCar").trigger('reset');
                    $("#brndName").focus();
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
            brandName: {
                required: 'Please enter Cars Brand Name',
                minlength: 'Cars Brand Name must contain at-least 2 characters'
            },
            modelName: {
                required: 'Please enter Cars Model Name',
                minlength: 'Cars Model Name must contain at-least 2 characters'
            },
            rcNumber: {
                required: 'Please enter RC Number',
                minlength: 'RC Number must contain at-least 2 characters'
            },
            perKmsCost: {
                required: 'Please enter Per KMS Cost',
                minlength: 'Per KMs Cost must contain at-least 2 digits',
                number: 'Enter Number only, no characters are allowed'
            },
            features: {
                required: 'Please type select features according to car details',
            },
            transmission: {
                required: 'Please select Transmission type',
            },
            fuelType: {
                required: 'Please select Fuel Type',
            },
            minKM: {
                required: 'Please enter minimum kms',
                number: 'Enter Number only, no characters are allowed'
            },
            priceAftrFreeKM: {
                required: 'Please enter Price after Free KMS',
                number: 'Enter Number only, no characters are allowed'
            },
            seatcap: {
                required: 'Please select seating capacity based on your Car'
            },
            carImg: {
                required: 'Please upload Car Image',
                accept: 'only jpg, jpeg, png, gif, svg, webp'
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
//======================================================================================




//======================================================================================
//Ajax for Adding Car Details


// document.getElementById("addCarBtn").addEventListener("click", function (event) {
//     ajaxCall(event)
// });


// function ajaxCall(event) {

//     console.log("Ajax Function is called!!!");
//     event.preventDefault()
    
//     var formData = new FormData();

//     //Checkbox Value
//     var featuresjs = [];
//     $.each($("input[name='features']:checked"), function () {
//         featuresjs.push($(this).val());
//     });

//     formData.append('brandName', $('#brndName').val());
//     formData.append('modelName', $('#mdlName').val());
//     formData.append('rcNumber', $('#rcNo').val());
//     formData.append('perKmsCost', $('#pkc').val());
//     formData.append('feat', featuresjs);
//     formData.append('minKM', $('#mink').val());
//     formData.append('seatcap', $('#sc').val());
//     formData.append('carImg', $('input[type=file]')[0].files[0]);
//     formData.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());

//     $.ajax({
//         type: 'POST',
//         url: 'addcar',
//         data: formData,
//         cache: false,
//         processData: false,
//         contentType: false,
//         enctype: 'multipart/form-data',
//         success: function() {
//             alert('Car Added!');
//         },
//         error: function(xhr, errmsg, err) {
//             console.log(xhr.status + ":" + xhr.responseText)
//         }
//     })

// }
