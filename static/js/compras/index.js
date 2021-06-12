/* Seccion Proveedor */

function list_proveedor(url_list, url_edit, url_del, perm_change, perm_delete) {
    $('#provTable').DataTable({
        responsive: true,
        pageLength: 6,
        lengthMenu: [6, 10, 20],
        ajax: {
            url: url_list,
            type: 'GET',
            dataType: 'json',
            dataSrc: ''
        },
        columns: [
            {"data": "ruc"},
            {"data": "razon_social"},
            {"data": "telefono"},
            {"data": "email"},
            {"data": "direccion"},
            {"data": "id"},
        ],
        columnDefs: [{
            targets: [-1],
            orderable: false,
            render: function (data, type, row) {
                var buttons = ''
                if (perm_change) {
                    buttons += '<button onclick="abrir_modal(\'' + url_edit + row.id + '/\')" class="btn btn-warning btn-sm" title="Editar"><i class="fas fa-edit"></i></button> ';
                }
                if (perm_delete) {
                    buttons += '<button onclick="delete_ajax_prov(\'' + url_del + row.id + '/\')" title="Borrar" class="btn btn-danger btn-sm"><i class="fas fa-trash-alt"></i></button>';
                }
                return buttons;
            }
        }]
    });
}

function abrir_modal_prov(url) {
    $('#proveedorModal').load(url, function () {
        $(this).modal('show');
    });
}

function cerrar_modal_prov() {
    $('#proveedorModal').modal('hide');
}

function create_ajax_prov() {
    $.ajax({
        data: $('#provForm').serializeArray(),
        url: $('#provForm').attr('action'),
        type: $('#provForm').attr('method'),
        success: function (response) {
            cerrar_modal_prov();
            show_notify_success(response.message);
        },
        error: function (error) {
            console.log(error);
            show_error_form(error);
        }
    }).done(function () {
        $('#provTable').DataTable().ajax.reload();
    });
}

function editar_ajax_prov() {
    $.ajax({
        data: $('#provFormUpdate').serializeArray(),
        url: $('#provFormUpdate').attr('action'),
        type: $('#provFormUpdate').attr('method'),
        success: function (response) {
            cerrar_modal_prov();
            show_notify_success(response.message);
        },
        error: function (error) {
            console.log(error);
            show_error_form(error);
        }
    }).done(function () {
        $('#provTable').DataTable().ajax.reload();
    });
}

function delete_ajax_prov(url) {
    Swal.fire({
        title: '¿Estás se seguro de querer eliminar éste proveedor?',
        text: "Este cambio no puede ser revertido",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar!'
    }).then((result) => {
        if (result.isConfirmed) {
            let csrf = {}
            csrf['csrfmiddlewaretoken'] = $('input[name="csrfmiddlewaretoken"]').val();
            $.ajax({
                url: url,
                type: 'post',
                data: csrf,
                success: function () {
                    $('#provTable').DataTable().ajax.reload();
                    Swal.fire(
                        '¡Eliminado!',
                        'Este proveedor ha sido eliminado',
                        'success'
                    );
                },
                error: function (error) {
                    console.log(error);
                }
            })

        }
    })
}

/*
 * Funcion para crear factura compra por medio de ajax
 * */
function create_ajax_factura(url, type, data, redirect) {
    Swal.fire({
        title: 'Registro Factura',
        text: "¿Desea guardar la factura?",
        icon: 'info',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: '¡Si, guardar!'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                type: 'POST',
                data: data,
                datatype: type,
                url: url,
                processData: false,
                contentType: false,
                success: function (response) {
                    mensaje_success('Factura Compra', response.message);
                    location.href = redirect;
                },
                error: function (error) {
                    show_error_json(error);
                }
            });
        }
    });
}