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

/* REGISTER FORM */

$("#id_email").blur(function() {
  $(this).attr('placeholder', "*Correo electrónico").placeholder();
});

$("#id_first_name").blur(function() {
  $(this).attr('placeholder', "*Nombre").placeholder();
});

$("#id_last_name").blur(function() {
  $(this).attr('placeholder', "*Apellido").placeholder();
});

$("#id_phone").blur(function() {
  $(this).attr('placeholder', "Teléfono").placeholder();
});

$("#id_dni").blur(function() {
  $(this).attr('placeholder', "*DNI").placeholder();
});

$("#id_city").blur(function() {
  $(this).attr('placeholder', "Ciudad").placeholder();
});

$("#id_address").blur(function() {
  $(this).attr('placeholder', "Dirección").placeholder();
});

$("#id_password1").blur(function() {
  $(this).attr('placeholder', "Contraseña").placeholder();
});

$("#id_password2").blur(function() {
  $(this).attr('placeholder', "Repita contraseña").placeholder();
});

/* LOGIN */

$("#id_username").blur(function() {
  $(this).attr('placeholder', "Correo electrónico").placeholder();
});

$("#id_password").blur(function() {
  $(this).attr('placeholder', "Contraseña").placeholder();
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

/* currency converter functions */

function convertCurrency() {
  
  var from = document.getElementById("from").value;
  var to = document.getElementById("to").value;
  var xmlhttp = new XMLHttpRequest();
  var url = "http://data.fixer.io/api/latest?access_key=bf27415b8a1d95b6cde0a5a4c5794277&symbols=" + from + "," + to;
  xmlhttp.open("GET", url, true);
  xmlhttp.send();
  xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
      var result = xmlhttp.responseText;
      var jsResult = JSON.parse(result);
      var oneUnit = jsResult.rates[to]/jsResult.rates[from];
      var amt = document.getElementById("fromAmount").value;
      document.getElementById("toAmount").value = (oneUnit*amt).toFixed(2);
    }
  }

}
