/*jshint browser:true */
/*global $ */(function()
{
    "use strict";
    /*
    hook up event handlers 
    */
    function register_event_handlers()
    {
        $('#btn-save').click(function(){
            var ip = $('#ip').val();
            var porta = $('#porta').val();
            var response;
         
            if(ip.length < 7 || ip === null){
              
                navigator.notification.alert('O endereço IP está incorreto!');
              
            } else {
                if(porta.length === 0 || porta == null){
                    response = writeFile('config.txt', ip+':5000');
                } else {
                    response = writeFile('config.txt', ip+':'+ porta);
                }
                navigator.notification.alert(response);
            }
        });
    }
    document.addEventListener("app.Ready", register_event_handlers, false);
})();
