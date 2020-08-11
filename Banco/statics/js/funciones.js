$("input").focus(function() {
      $(this).removeAttr('placeholder');
});

$("#ing").blur(function() {
      $(this).attr('placeholder', "Monto").placeholder();
});

$("#name").blur(function() {
      $(this).attr('placeholder', "Nombre").placeholder();
});

$("#lastname").blur(function() {
      $(this).attr('placeholder', "Apellido").placeholder();
});

$("#email").blur(function() {
      $(this).attr('placeholder', "example@gmail.com").placeholder();
});

$("#search-input").blur(function() {
  $(this).attr('placeholder', "Buscar personas").placeholder();
});

$("#trans-cant").blur(function() {
  $(this).attr('placeholder', "$").placeholder();
});

$("#trans-cvu").blur(function() {
  $(this).attr('placeholder', "CVU").placeholder();
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
    var texarea = $('textarea').val();

    if (texarea == "") {
      
    } else {
      $("#mostrarmodal2").modal("show");
      $("#mostrarmodal").modal("hide");
      $('#texarea').val('');
    }
  });
