/* Seccion Cliente */

function list_cliente(url_list, url_edit, url_del) {
    $('#clienteTable').DataTable({
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
            {"data": "cedula"},
            {"data": "nombre"},
            {"data": "apellido"},
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
                var buttons = '<button onclick="abrir_modal(\'' + url_edit + row.id + '/\')" class="btn btn-warning btn-sm" title="Editar"><i class="fas fa-edit"></i></button> ';
                buttons += '<button onclick="delete_ajax_cliente(\'' + url_del + row.id + '/\')" title="Borrar" class="btn btn-danger btn-sm"><i class="fas fa-trash-alt"></i></button>';
                return buttons;
            }
        }]
    });
}

function abrir_modal(url) {
    $('#clienteModal').load(url, function () {
        $(this).modal('show');
    });
}

function cerrar_modal() {
    $('#clienteModal').modal('hide');
}

function create_ajax_cliente() {
    $.ajax({
        data: $('#clienteForm').serializeArray(),
        url: $('#clienteForm').attr('action'),
        type: $('#clienteForm').attr('method'),
        success: function (response) {
            cerrar_modal();
            show_notify_success(response.message);
        },
        error: function (error) {
            console.log(error);
            show_error_form(error);
        }
    }).done(function () {
        $('#clienteTable').DataTable().ajax.reload();
    });
}

function editar_ajax_cliente() {
    $.ajax({
        data: $('#clienteFormUpdate').serializeArray(),
        url: $('#clienteFormUpdate').attr('action'),
        type: $('#clienteFormUpdate').attr('method'),
        success: function (response) {
            cerrar_modal();
            show_notify_success(response.message);
        },
        error: function (error) {
            console.log(error);
            show_error_form(error);
        }
    }).done(function () {
        $('#clienteTable').DataTable().ajax.reload();
    });
}

function delete_ajax_cliente(url) {
    Swal.fire({
        title: '¿Estás se seguro de querer eliminar éste cliente?',
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
                    $('#clienteTable').DataTable().ajax.reload();
                    Swal.fire(
                        '¡Eliminado!',
                        'Este cliente ha sido eliminado',
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