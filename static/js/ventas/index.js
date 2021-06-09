/* Seccion Cliente */
function list_cliente(url_list, url_edit,url_del) {
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



//SECCION VENTAS/FACTURAS

function list_factura(url_list,url_del) {
    $('#facturaTable').DataTable({
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
            {"data": "nro_factura"},
            {"data": "cliente"},
            {"data": "fecha_emision"},
            {"data": "estado"},
            {"data": "total"},
            {"data": "id"},
        ],
        columnDefs: [{
        targets: [-1],
        orderable: false,
        render: function (data, type, row) {
            var buttons = '<a href="/modulos/ventas/facturas/edit/' + row.id + '/" class="btn btn-warning btn-xs btn-sm"><i class="fas fa-edit"></i></a> ';

            buttons += '<button onclick="abrir_modal_cobro(\''+ row.id + '\')" title="Cuotas" class="btn btn-success btn-sm"><i class="fas fa-search"></i></button>';
            buttons += '<a href="/modulos/ventas/facturas/invoice/pdf/' + row.id + '/" class="btn btn-primary btn-xs btn-sm"><i class="fas fa-print"></i></a> ';
            buttons += '<button onclick="delete_ajax_factura(\'' + url_del + row.id + '/\')" title="Borrar" class="btn btn-danger btn-sm"><i class="fas fa-trash-alt"></i></button>';


           return buttons;
        }
        }]
    });

   
}

function abrir_modal_cobro(row) {
    $('#cobroDet').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        //data: data.det,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_details_cobro',
                'id': row
            },
            dataSrc: ""
        },
        columns: [
            {"data": "nro_cuota"},
            {"data": "monto_cuota"},
            {"data": "estado"},
            {"data": "fecha_vencimiento"},
            {"data": "fecha_pago"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [1],
                class: 'text-center',
                render: function (data, type, row) {
                    return 'Gs ' + row.monto_cuota ;
                }
            },
            {
                targets: [2],
                class: 'text-center',
                render: function (data, type, row) {
                    var $select = $("<select class='form-control' id='estadoCuota'><option value='PAGADA'>PAGADA</option><option value='PENDIENTE'>PENDIENTE</option></select>");
                    $select.find('option[value="'+row.estado+'"]').attr('selected', 'selected');
                    return $select[0].outerHTML
                }
            },
            {
                targets: [5],
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '<button onclick="actualizar_cuota(\''+ row.id + '\')" title="Guardar" class="btn btn-success btn-sm"><i class="fas fa-save"></i></button>';
                    return buttons;
                }
            },

        ],
        initComplete: function (settings, json) {

        }
    });
    $('#modalCobro').modal('show');


}

function actualizar_cuota(id) {
    var estado=$('#estadoCuota').val();
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'edit_cuota',
            'cuota_id':id,
            'estado':estado,

        },
        dataType: 'json',
    }).done(function (data) {
        $('#modalCobro').modal('hide');
        show_notify_success('La cuota ha sido modificada!');
        $('#facturaTable').DataTable().ajax.reload();
    }).fail(function (jqXHR, textStatus, errorThrown) {
        //alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {

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
                    $('#facturaTable').DataTable().ajax.reload();
                    Swal.fire(
                        '¡Eliminado!',
                        'Esta factura ha sido eliminada',
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

