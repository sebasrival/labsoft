

function alert_delete(title, content, callback){
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