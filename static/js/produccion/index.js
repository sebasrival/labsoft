/* Seccion producto */
function list_orden(url_list, url_edit, url_del, perm_change, perm_delete) {
    $('#ordenTable').DataTable({
        responsive: true,
        pageLength: 6,
        lengthMenu: [6, 10, 20],
        ajax: {
            url: url_list,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "numero"},
            {"data": "estado"},
            {"data": "fecha_emision"},
            {"data": "fecha_vigencia"},
            {"data": "producto"},
            {"data": "cantidad_teorica"},
            {"data": "id"},
        ],
        columnDefs: [{
        targets: [-1],
        orderable: false,
        render: function (data, type, row) {
            let buttons = '';
            if (perm_change){
                buttons += '<a href="'+ url_edit + row.id + '/" class="btn btn-warning btn-xs btn-sm"><i class="fas fa-edit"></i></a> ';
            }
            if(perm_delete){
                buttons += '<button onclick="delete_ajax_orden(\'' + url_del + row.id + '/\')" title="Borrar" class="btn btn-danger btn-sm"><i class="fas fa-trash-alt"></i></button>';
            }



           return buttons;
        }
        }]
    });
}

function delete_ajax_orden(url) {
    Swal.fire({
        title: '¿Estás se seguro de querer eliminar ésta orden?',
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
                    $('#ordenTable').DataTable().ajax.reload();
                    Swal.fire(
                        '¡Eliminado!',
                        'Esta orden ha sido eliminada',
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

function list_formula(url_list, url_edit, url_del, perm_change, perm_delete) {
    $('#formTable').DataTable({
        responsive: true,
        pageLength: 6,
        lengthMenu: [6, 10, 20],
        ajax: {
            url: url_list,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ''
        },
        columns: [
            {"data": "producto"},
            {"data": "cantidad_teorica"},
            {"data": "id"},
        ],
        columnDefs: [{
            targets: [-1],
            orderable: false,
            render: function (data, type, row) {
                let buttons = ''
                console.log(perm_change)
                if (perm_change){
                    buttons += '<a href="' + url_edit + row.id + '/" class="btn btn-warning btn-xs btn-sm"><i class="fas fa-edit"></i></a> ';
                }
                if(perm_delete){
                    buttons += '<button onclick="delete_ajax_formula(\'' + url_del + row.id + '/\')" title="Borrar" class="btn btn-danger btn-sm"><i class="fas fa-trash-alt"></i></button>';
                }
                return buttons;
            }
        }]
    });
}
function delete_ajax_formula(url) {
    Swal.fire({
        title: '¿Estás se seguro de querer eliminar ésta formula?',
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
                    $('#formTable').DataTable().ajax.reload();
                    Swal.fire(
                        '¡Eliminado!',
                        'Esta formula ha sido eliminado',
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
function list_producto(url_list, url_edit, url_del, perm_change, perm_delete) {
    $('#productoTable').DataTable({
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
            {"data": "codigo_producto"},
            {"data": "nombre"},
            {"data": "tipo"},
            {"data": "color"},
            {"data": "precio"},
            {"data": "cantidad_contenido"},
            {"data": "cantidad"},
            {"data": "id"},
        ],
        columnDefs: [{
            targets: [-1],
            orderable: false,
            render: function (data, type, row) {
                let buttons = ''
                console.log(perm_change)
                if (perm_change){
                    buttons += '<button onclick="abrir_modal(\'' + url_edit + row.id + '/\')" class="btn btn-warning btn-sm" title="Editar"><i class="fas fa-edit"></i></button> ';
                }
                if(perm_delete){
                    buttons += '<button onclick="delete_ajax_producto(\'' + url_del + row.id + '/\')" title="Borrar" class="btn btn-danger btn-sm"><i class="fas fa-trash-alt"></i></button>';
                }
                return buttons;
            }
        }]
    });
}

function abrir_modal(url) {
    $('#productoModal').load(url, function () {
        $(this).modal('show');
    });
}

function cerrar_modal() {
    $('#productoModal').modal('hide');
}

function create_ajax_producto() {
    $.ajax({
        stock: $('#cantidadStock').val(),
        data: $('#productoForm').serializeArray(),
        url: $('#productoForm').attr('action'),
        type: $('#productoForm').attr('method'),
        success: function (response) {
            cerrar_modal();
            show_notify_success(response.message);
        },
        error: function (error) {
            console.log(error);
            show_error_form(error);
        }
    }).done(function () {
        $('#productoTable').DataTable().ajax.reload();
    });
}

function editar_ajax_producto() {
    $.ajax({
        data: $('#productoFormUpdate').serializeArray(),
        url: $('#productoFormUpdate').attr('action'),
        type: $('#productoFormUpdate').attr('method'),
        success: function (response) {
            cerrar_modal();
            show_notify_success(response.message);
        },
        error: function (error) {
            console.log(error);
            show_error_form(error);
        }
    }).done(function () {
        $('#productoTable').DataTable().ajax.reload();
    });
}

function delete_ajax_producto(url) {
    Swal.fire({
        title: '¿Estás se seguro de querer eliminar éste producto?',
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
                    $('#productoTable').DataTable().ajax.reload();
                    Swal.fire(
                        '¡Eliminado!',
                        'Este producto ha sido eliminado',
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

