function list_proveedor(url) {
    $('#provTable').DataTable({
        responsive: true,
        pageLength: 6,
        lengthMenu: [6, 10, 20],
        ajax: {
            url: url,
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
                var buttons = '<button class="btn btn-warning btn-sm" title="Editar"><i class="fas fa-edit"></i></button> ';
                buttons += '<button title="Borrar" class="btn btn-danger btn-sm"><i class="fas fa-trash-alt"></i></button>';
                return buttons;
            }
        }]
    });
}

function abrir_modal(url) {
    $('#proveedorModal').load(url, function () {
        $(this).modal('show');
    });
}

function cerrar_modal(){
    $('#proveedorModal').modal('hide');
}

function create_ajax_prov() {
    $.ajax({
        data: $('#provForm').serializeArray(),
        url: $('#provForm').attr('action'),
        type: $('#provForm').attr('method'),
        success: function () {
            cerrar_modal();
        },
        error: function (error) {
            console.log(error);
        }
    }).done(function () {
        $('#provTable').DataTable().ajax.reload();
    })
}
