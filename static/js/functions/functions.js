/*
* Tira una alerta de eliminacion tiene
* callback es la funcion que recibe para luego de la acción
* */
function alert_delete(title, content, callback) {
    swal({
        title: title,
        text: content,
        type: "warning",
        showCancelButton: true,
        confirmButtonText: "Si, eliminar!",
        cancelButtonText: "Cancelar!",
        closeOnConfirm: false,
        closeOnCancel: false
    }, function (isConfirm) {
        if (isConfirm) {
            swal({
                title: "Eliminado",
                type: "success"
            }, function () {
                callback();
            });
        } else {
            swal("Cancelado", "", "error");
        }
    });
}

/*
*Para enviar datos del formulario con ajax
* */
function submit_with_ajax(url, title, content, parameters, callback) {
    swal({
        title: title,
        text: content,
        type: "warning",
        showCancelButton: true,
        confirmButtonText: "Si, registrar!",
        cancelButtonText: "Cancelar!",
        closeOnConfirm: false,
        closeOnCancel: false
    }, function (isConfirm) {
        if (isConfirm) {
            console.log(url);
            $.ajax({
                url: url,
                type: 'POST',
                data: parameters,
                dataType: 'json',
                processData: false,
                contentType: false,
                success: function () {
                    swal({
                        title: 'Notificación',
                        text: 'Se ha Registrado Correctamente',
                        type: 'success'
                    }, function () {
                        callback();
                    });
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    swal("Error", xhr + ' ' + ajaxOptions + ' ' + thrownError , "error");
                }
            });
        } else {
            swal("Cancelado", "", "error");
        }
    });
}