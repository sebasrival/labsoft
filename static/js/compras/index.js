function list_proveedor() {
    $('#provTable').DataTable({
        responsive: true,
        destroy: true,
        pageLength: 6,
        lengthMenu: [6, 10, 20],
        ajax: {
            url: window.location.pathname,
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
        columnDefs:[{
            targets: [-1],
            orderable: false,
            render: function (data, type, row){
                var buttons = '<button class="btn btn-warning btn-sm" title="Editar"><i class="fas fa-edit"></i></button> ';
                buttons += '<button title="Borrar" class="btn btn-danger btn-sm"><i class="fas fa-trash-alt"></i></button>';
                return buttons;
            }
        }]
    });
}

