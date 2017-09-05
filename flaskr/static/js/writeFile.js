function writeFile(str_filename, str_text) {
    var type = window.PERSISTENT;
    var size = 5*1024*1024;
    var response;

    window.requestFileSystem(type, size, successCallback, errorCallback)

    function successCallback(fs) {

        fs.root.getFile(str_filename, {create: true}, function(fileEntry) {
            
            fileEntry.createWriter(function(fileWriter) {
                fileWriter.onwriteend = function(e) {
                    response = {'status':true,'message':'Salvo com sucesso'};
                };

                fileWriter.onerror = function(e) {
                    response = {'status':false,'message':'Falha ao salvar:' + e.toString()};
                };

                var blob = new Blob([str_text], {type: 'text/plain'});
                fileWriter.write(blob);
            }, errorCallback);

        }, errorCallback);

   }

   function errorCallback(error) {
      response = "ERROR: " + error.code;
   }
    return response;
}