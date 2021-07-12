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
                    buttons += '<button onclick="abrir_modal_prov(\'' + url_edit + row.id + '/\')" class="btn btn-warning btn-sm" title="Editar"><i class="fas fa-edit"></i></button> ';
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

// seccion stock
function list_stock(url_list, url_edit, url_del, perm_change, perm_delete) {
    $('#stockTable').DataTable({
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
            {"data": "materia"},
            {"data": "cantidad_stock"},
            {"data": "unidad_medida"},

            {"data": "id" }
        ],
        columnDefs: [{
            targets: [-1],
            orderable: false,
            render: function (data, type, row) {
                var buttons = ''
                if (perm_change) {
                    buttons += '<button onclick="abrir_modal_stock(\'' + url_edit + row.id + '/\')" class="btn btn-warning btn-sm" title="Editar"><i class="fas fa-edit"></i></button> ';
                }
                if (perm_delete) {
                    buttons += '<button onclick="delete_ajax_stock(\'' + url_del + row.id + '/\')" title="Borrar" class="btn btn-danger btn-sm"><i class="fas fa-trash-alt"></i></button>';
                }
                return buttons;
            }
        }]
    });
}

function abrir_modal_stock(url) {
    $('#stockModal').load(url, function () {
        $(this).modal('show');
    });
}

function cerrar_modal_stock(){
    $('#stockModal').modal('hide');
}

function create_ajax_stock(){
    $.ajax({
        data: $('#stockForm').serializeArray(),
        url: $('#stockForm').attr('action'),
        type: $('#stockForm').attr('method'),
        success: function (response) {
            cerrar_modal_stock();
            show_notify_success(response.message);
        },
        error: function (error) {
            console.log(error);
            show_error_form(error);
        }
    }).done(function () {
        $('#stockTable').DataTable().ajax.reload();
    });
}

function editar_ajax_stock(){
    $.ajax({
        data: $('#stockFormUpdate').serializeArray(),
        url: $('#stockFormUpdate').attr('action'),
        type: $('#stockFormUpdate').attr('method'),
        success: function (response) {
            cerrar_modal_stock();
            show_notify_success(response.message);
        },
        error: function (error) {
            console.log(error);
            show_error_form(error);
        }
    }).done(function () {
        $('#stockTable').DataTable().ajax.reload();
    });
}

function delete_ajax_stock(url) {
    Swal.fire({
        title: '¿Estás se seguro de querer eliminar éste stock?',
        text: "Este cambio no puede ser revertido",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar!'
    }).then((result) => {
        if (result.isConfirmed) {
            let csrf = {};
            csrf['csrfmiddlewaretoken'] = $('input[name="csrfmiddlewaretoken"]').val();
            $.ajax({
                url: url,
                type: 'post',
                data: csrf,
                success: function () {
                    $('#stockTable').DataTable().ajax.reload();
                    Swal.fire(
                        '¡Eliminado!',
                        'Este stock ha sido eliminado',
                        'success'
                    );
                },
                error: function (error) {
                    console.log(error);
                }
            });

        }
    });
}


/* Seccion Facturas*/
function list_factura(url_list, url_edit, url_del, perm_change, perm_delete) {
    /* Listar Factura */
    console.log(url_del);
    $('#factTable').DataTable({
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
            {"data": "nro_factura"},
            {"data": "tipo_factura"},
            {"data": "fecha_factura"},
            {"data": "estado"},
            {"data": "pago"},
            {"data": "total"},
            {"data": "id"},
        ],
        columnDefs: [
        {
            targets: [3],
            orderable: false,
            render: function (data, type, row) {
                if (row.estado === 'RECIBIDO'){
                    return '<span style="background-color: green; color: white; font-weight: bold;">'+ row.estado +'</span>'
                }else{
                    return '<span style="background-color: red; color:white; font-weight: bold;">'+ row.estado +'</span>'
                }
            }
        },
        {
            targets: [-1],
            orderable: false,
            render: function (data, type, row) {
                let buttons = '';
                if (perm_change) {
                    buttons += '<a href="'+ url_edit + row.id + '" class="btn btn-warning btn-sm" title="Editar"><i class="fas fa-edit"></i></a> ';
                }
                if (perm_delete) {
                    buttons += '<button onclick="delete_ajax_factura(\'' + url_del + row.id + '/\')" title="Borrar" class="btn btn-danger btn-sm"><i class="fas fa-trash-alt"></i></button>';
                }
                return buttons;
            }
        }
        ]
    });
}

function create_ajax_factura(url, type, data, redirect) {
    /* Funcion para crear factura compra por medio de ajax */
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
                    mensaje_succes_func('Factura Compra', response.message, function () {
                        location.href = redirect
                    });
                },
                error: function (error) {
                    console.log(error);
                    mensaje_error('Error al Registrar', error.responseJSON.error);
                }
            });
        }
    });
}

function delete_ajax_factura(url) {
    Swal.fire({
        title: '¿Estás se seguro de querer eliminar ésta factura?',
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
                    $('#factTable').DataTable().ajax.reload();
                    Swal.fire(
                        '¡Eliminado!',
                        'Esta factura ha sido eliminada',
                        'success'
                    );
                },
                error: function (error) {
                    mensaje_error('Error al borrar', error)
                }
            })

        }
    })
}