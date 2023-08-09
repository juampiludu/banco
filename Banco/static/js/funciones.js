$(document).ready(function() {
  $('[data-bs-toggle="tooltip"]').tooltip();
});

function valida(e){
    tecla = (document.all) ? e.keyCode : e.which;

    if (tecla==8){
        return true;
    }

    patron =/[0-9.]/;
    tecla_final = String.fromCharCode(tecla);
    return patron.test(tecla_final);
}

// Initialize and add the map
function initMap() {
  // The location of Uluru
  var uluru = {lat: -31.25378, lng: -64.26068};
  // The map, centered at Uluru
  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 16, center: uluru});
  // The marker, positioned at Uluru
  var marker = new google.maps.Marker({position: uluru, map: map});
}

$('#btn3').click(function()
   {
      $("#mostrarmodal").modal("show");
   });

$('#btn4').click(function()
  {

    if ($("#motivo").val() != "") {

      $("#mostrarmodal2").modal("show");
      $("#mostrarmodal").modal("hide");
      setTimeout(() => {$("#motivo").val("");}, 500)

    }

  });

  $('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
    if (!$(this).next().hasClass('show')) {
      $(this).parents('.dropdown-menu').first().find('.show').removeClass('show');
    }
    var $subMenu = $(this).next('.dropdown-menu');
    $subMenu.toggleClass('show');


    $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
      $('.dropdown-submenu .show').removeClass('show');
    });


    return false;
  });