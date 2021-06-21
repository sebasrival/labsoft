//Seccion equipos


function list_equipo(url_list, url_edit, url_del, perm_change, perm_delete) {
    $('#equipoTable').DataTable({
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
            {"data": "codigo"},
            {"data": "nombre"},
            {"data": "id"},
        ],
        columnDefs: [{
            targets: [-1],
            orderable: false,
            render: function (data, type, row) {
                let buttons = '';
                if (perm_change){
                    buttons += '<button onclick="abrir_modal(\'' + url_edit + row.id + '/\')" class="btn btn-warning btn-sm" title="Editar"><i class="fas fa-edit"></i></button> ';
                }
                if (perm_delete){
                    buttons += '<button onclick="delete_ajax_equipo(\'' + url_del + row.id + '/\')" title="Borrar" class="btn btn-danger btn-sm"><i class="fas fa-trash-alt"></i></button>';
                }
                return buttons;
            }
        }]
    });
}

function abrir_modal(url) {
    $('#equipoModal').load(url, function () {
        $(this).modal('show');
    });
}

function cerrar_modal() {
    $('#equipoModal').modal('hide');
}

function create_ajax_equipo() {
    $.ajax({
        data: $('#equipoForm').serializeArray(),
        url: $('#equipoForm').attr('action'),
        type: $('#equipoForm').attr('method'),
        success: function (response) {
            cerrar_modal();
            show_notify_success(response.message);
        },
        error: function (error) {
            console.log(error);
            show_error_form(error);
        }
    }).done(function () {
        $('#equipoTable').DataTable().ajax.reload();
    });
}

function editar_ajax_equipo() {
    $.ajax({
        data: $('#equipoFormUpdate').serializeArray(),
        url: $('#equipoFormUpdate').attr('action'),
        type: $('#equipoFormUpdate').attr('method'),
        success: function (response) {
            cerrar_modal();
            show_notify_success(response.message);
        },
        error: function (error) {
            console.log(error);
            show_error_form(error);
        }
    }).done(function () {
        $('#equipoTable').DataTable().ajax.reload();
    });
}

function delete_ajax_equipo(url) {
    Swal.fire({
        title: '¿Estás se seguro de querer eliminar éste equipo?',
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
                    $('#equipoTable').DataTable().ajax.reload();
                    Swal.fire(
                        '¡Eliminado!',
                        'Este equipo ha sido eliminado',
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