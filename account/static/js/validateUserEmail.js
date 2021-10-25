//Check Username - Registration Form

$("#username").change(function () {
  var username = $(this).val();

  $.ajax({
    url: 'checkUsername',
    data: {
      'username':username
    },
    dataType: 'json',
    success: function (data) {
      if (data.is_present) {
        var ufe = $("#ufieldErr");
        ufe.append("<span class='username_error1'>Username Not Available</span>")
        document.getElementById('submitBtn').disabled = true;
        $('.username_error').remove();
      }
      else {
        var ufe = $("#ufieldErr");
        ufe.append("<span class='username_error'>Username  Available</span>")
        $('.username_error1').remove();
        document.getElementById('submitBtn').disabled = false;
      }
    }
  })

})




//Check Email-ID - Registration Form

$("#email").change(function () {
  var email = $(this).val();

  $.ajax({
    url: 'checkEmailID',
    data: {
      'email':email
    },
    dataType: 'json',
    success: function (data) {
      if (data.is_present) {
        var efe = $("#efieldErr");
        efe.append("<span class='username_error1'>Email ID is already in used.</span>")
        document.getElementById('submitBtn').disabled = true;
        $('.username_error').remove();
      }
      else {
        var efe = $("#efieldErr");
        efe.append("<span class='username_error'>Email ID is Available</span>");
        $('.username_error1').remove();
        document.getElementById('submitBtn').disabled = false;
      }
    }
  })

})



//Check Email-ID for Change Password

$("#emailOne").change(function () {
  var email = $(this).val();

  $.ajax({
    url: 'cpCheckEmail',
    data: {
      'email':email
    },
    dataType: 'json',
    success: function (data) {
      if (data.is_present) {
        var efe = $("#efieldErr");
        efe.append("<span class='username_error'>Email ID Match</span>")
        $('.username_error1').remove();
        document.getElementById('submitBtn').disabled = false;
      }
      else {
        var efe = $("#efieldErr");
        efe.append("<span class='username_error1'>Email ID does not match, please re-check your Email ID.</span>")
        document.getElementById('submitBtn').disabled = true;
        $('.username_error').remove();
      }
    }
  })

})
