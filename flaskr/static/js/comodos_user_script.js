$(document).ready(function() {

    
     var get = getRouteParameter();
     var id = get.id;
     //nao necessario a url toda no site
     (function update() {
         // body...
         $.ajax({
            url: "/devices",
            type: 'POST',
            data: {id:id},
            dataType: "json",
            success: function(result){
            
                var content = '<div class="col-xs-12"><h3> '+ result[0].comodo + ' </h3></div>';
                var nome = "";
                var dispositivo = "";
                var button = "";
                var acao = "";
                var edit = "";
                var aparelhos = result[1].aparelhos;
                for(var i = 0; i < aparelhos.length; i++) {
                    // edit = '<div class="row text-right"><a href="/edit_device?id='+aparelhos[i].id+'" class="btn btn-xs btn-default btn-edit"><i class="glyphicon glyphicon-pencil"></i></a></div>';
                    nome = '<h5>' + aparelhos[i].name + '</h5>';

                    dispositivo = '<h1><i class="glyphicon glyphicon-lamp"></i></h1>';

                    if(aparelhos[i].status == 1) {

                        button = '<button class="btn btn-default btn-block btn-lg btn-equipamento btn-on" data-estado="0" data-id="' + aparelhos[i].id + '">';

                        status = '<p class="status">status: <span class="text-success">Ligado</span></p>';

                        acao = '<p class="acao">Desligar</p>';

                    } else {

                        button = '<button class="btn btn-default btn-block btn-lg btn-equipamento btn-off" data-estado="1" data-id="' + aparelhos[i].id + '">';

                        status = '<p class="status">status: <span class="text-danger">Desligado</span></p>';

                        acao = '<p class="acao">Ligar</p>';

                    }


                    content = content + '<div class="col-xs-12 col-sm-6 col-md-4">'/*+ edit*/ + button + nome + status + dispositivo + acao + ' </button> </div>';

                }

                $('#content').html(content);
                
                
                
                $('.btn-equipamento').click(function(){

                    var estado = $(this).data('estado');
                    var aparelho_id = $(this).data('id');

                    var status = $(this).children('.status');
                    var acao = $(this).children('.acao');
                    var span = status.children('span');
                    
                    var equipamento = $(this);
                    
                    $.ajax({
                    
                        url: "/swap",
                        type:'POST',
                        data: {id:aparelho_id, estado:estado},
                        dataType: "json",
                        success: function(response){
                            
                            console.log(response);
                            if(response.status == '0') {
                                equipamento.data('estado','1');
                                equipamento.addClass('btn-off').removeClass('btn-on');
                                span.addClass('text-danger').removeClass('text-success');
                                span.html('Desligado');
                                acao.html('Ligar');

                            } else {
                                equipamento.data('estado','0');
                                equipamento.addClass('btn-on').removeClass('btn-off');
                                span.addClass('text-success').removeClass('text-danger');
                                span.html('Ligado');
                                acao.html('Desligar');

                            }
                            
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
                           alert(msg);
                        },
                        complete: function(){
    //                        navigator.notification.alert("Completo!",  null, 'Resposta da Conexão', 'ok');
                        }

                    });

                    

                });
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
                            alert(msg);
            },
            complete: function(){
    //            navigator.notification.alert("Completo!",  null, 'Resposta da Conexão', 'ok');
            }
        }).then(function() {
           setTimeout(update,5000);
       });
       })();
    // body...
});
