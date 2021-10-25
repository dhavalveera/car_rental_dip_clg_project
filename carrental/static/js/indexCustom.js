document.addEventListener('DOMContentLoaded', function () {
    var options = {
        minDate: setMinDate(),
        autoClose: true,
        format: 'dd-mm-yyyy'
    }
    var elems = document.querySelectorAll('.datepicker');
    var instances = M.Datepicker.init(elems, options);
});


function setMinDate() {
  const today = moment();
  return new Date(today);
}


//Swiper Slider Initializer

var swiper = new Swiper('.swiper-container', {
  slidesPerView: 2,
  spaceBetween: 30,
  slidesPerGroup: 2,
  loop: true,
  loopFillGroupWithBlank: true,
  autoplay: {
    delay: 4000,
    disableOnInteraction: false,
  },
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
  },
});
