//Start of Navbar & Mobile Navbar JS Initialization Code

document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems);
});


//End of Navbar & Mobile Navbar JS Initialization Code


//Drop-Down Menu Trigger

$(".dropdown-trigger").dropdown();


//Collapsible Initializer
document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.collapsible');
    var instances = M.Collapsible.init(elems);
});

