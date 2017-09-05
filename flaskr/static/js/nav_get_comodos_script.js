$(document).ready(function() {

     /* button  #alertar */
     var rota = "/room";
    //nao necessario url toda   
    $.ajax({
        url: rota,
        dataType: "json",
        success: function(result){
        
            var navli = "";
          

            for(var i = 0; i < result.length; i++) {
               
                navli = navli + '<li><a href="/comodos?id=' + result[i].id + '">' +  result[i].nome; + '</a></li>';
                
            }

            $('#menu .navbar-nav').append(navli);
            
        },
         error:function (jqXHR, exception) {
                        var msg = '';
                        if (jqXHR.status === 0) {
                            msg = 'Not connect.\n Verify Network.';
                        } else if (jqXHR.status == 404) {
                            msg = 'Requested page not found. [404]';
                        } else if (jqXHR.status == 500) {
                            msg = 'Internal Server Error [500].';
                        } else if (exception === 'parsererror') {
                            msg = 'Requested JSON parse failed.';
                        } else if (exception === 'timeout') {
                            msg = 'Time out error.';
                        } else if (exception === 'abort') {
                            msg = 'Ajax request aborted.';
                        } else {
                            msg = 'Uncaught Error.\n' + jqXHR.responseText;
                        }
                       alert(msg + 'rota: ' + rota);
        },
        complete: function(){
//            navigator.notification.alert("Completo!",  null, 'Resposta da Conexão', 'ok');
        }
    });
    
 });
