/*--------------------
        * Type It
    ----------------------*/
new TypeIt("#dp", {
    strings: [
        'Delete My Account',
    ],
    speed: 200,
    loop: true,
    breakLines: false
}).go();



//Sweet Alert
$('#submitBtn').click(function() {
    swal({
        title: "Delete Account!",
        text: "Are you sure to delete your Account",
        icon: "warning",
        buttons: {
            cancel: true,
            confirm: true,
        },
        closeOnClickOutside: true,
        closeOnEsc: true,
    });
});