$("input").focus(function() {
      $(this).removeAttr('placeholder');
});

$("#user").blur(function() {
      $(this).attr('placeholder', "Nombre de Usuario").placeholder();
});

$("#pwd").blur(function() {
      $(this).attr('placeholder', "Contraseña").placeholder();
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
  $(this).attr('placeholder', "Buscar").placeholder();
});

$("#trans-cant").blur(function() {
  $(this).attr('placeholder', "$").placeholder();
});

$("#trans-cvu").blur(function() {
  $(this).attr('placeholder', "CVU").placeholder();
});

function copyCvu(elementId) {
  
  var aux = document.createElement("input");

  aux.setAttribute("value", document.getElementById(elementId).innerHTML);

  document.body.appendChild(aux);

  aux.select();

  document.execCommand("copy");

  document.body.removeChild(aux);

  alert("Ya tenés el CVU! Ahora andá a \"Saldo\" y pegá el número (" + aux.value + ") en el campo correspondiente.")

}

function abrir() {
  var usuar = document.getElementById("user").value;
  var contra = document.getElementById("pwd").value;
  if (usuar == "" || contra == ""){
    alert("Debe ingresar un nombre de usuario y/o contraseña");
  } else {
    window.location='template/home.html';
    alert("Bienvenido, " + usuar + "!");
  }
}

function abrir2() {
  window.location='template/home.html';
}

function valida(e){
    tecla = (document.all) ? e.keyCode : e.which;

    if (tecla==8){
        return true;
    }

    patron =/[0-9]/;
    tecla_final = String.fromCharCode(tecla);
    return patron.test(tecla_final);
}

function ingresar() {
  if (document.getElementById("ing").value == "") {
    alert("Ingrese el monto a agregar a su cuenta");
  } else {
    document.getElementById("ing").value = "";
  }
}

function retirar() {
  if (document.getElementById("ret").value == "") {
    alert("Ingrese el monto a retirar de su cuenta");
  }
  else if (document.getElementById("ret").value > document.getElementById("sa").value) {
    alert("Saldo insuficiente");
    document.getElementById("ret").value = "";
  } else {
        document.getElementById("ret").value = "";
      }
}

$('#btn3').click(function()
   {
      $("#mostrarmodal").modal("show");
   });

$('#btn4').click(function()
  {
    var nombre = $('#name').val();
    var apellido = $('#lastname').val();
    var email = $('#email').val();
    var texarea = $('textarea').val();

    if (nombre == "" || apellido == "" || email == "" || texarea == "") {
      alert("Completá todos los campos");
    } else {
      $("#mostrarmodal2").modal("show");
      $('#name').val('');
      $('#lastname').val('');
      $('#email').val('');
      $('#texarea').val('');
    }
  });
