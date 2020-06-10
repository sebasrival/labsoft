var tblPedidos;

// Estructura para el detalle de pedidos
var pedidos = {
    items: {
        cliente: '',
        fecha_pedido: '',
        fecha_entrega: '',
        total_pedido: 0.00,
        products: []
    },
    calc_invoice: function () {
        var subtotal = 0.00
        $.each(this.items.products, function (pos, dict) {
            dict.subtotal = dict.cantidad * parseFloat(dict.precio);
            subtotal += dict.subtotal;
        })
        this.items.total_pedido = subtotal;
        $('#subtotal').val(this.items.total_pedido.toFixed(2));
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        this.calc_invoice()
        tblPedidos = $('#tblPedidos').DataTable({
            responsive: true,
            destroy: true,
            data: this.items.products,
            ordering: false,
            columns: [
                {"data": "codigo_producto"},
                {"data": "nombre"},
                {"data": "description"},
                {"data": "precio"},
                {"data": "cantidad"},
                {"data": "subtotal"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [3, 5],
                    class: "text-center",
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [4],
                    width: "100%",
                    class: "text-center",
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
                    }
                },
                {
                    targets: [6],
                    class: "text-center",
                    width: "5%",
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger m-0 p-0"><i class="fa fa-trash m-1" aria-hidden="true"></i>\n</i></a>'
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 0,
                    max: 1000000000,
                    step: 1,
                    boostat: 5,
                    maxboostedstep: 10,
                }).keypress(function (e) {
                    return validate_form_text('numbers', e, null);
                });
            },
        });
    }
}

$('#search').on('select2:select', function (e) {
    var data = e.params.data;
    data['cantidad'] = 1;
    data['subtotal'] = 0.00;
    //se agrega los datos a la estructura
    pedidos.add(data)
    // borra luego de la seleccion
    $(this).val('').trigger('change.select2');
});

$('.btnRemoveAll').on('click', function () {
    if (pedidos.items.products.length === 0) return false;
    alert_delete('Notificación', '¿Estás seguro de eliminar todos los detalles del pedido', function () {
        pedidos.items.products = [];
        pedidos.list();
    });
});


$('#tblPedidos').on('click', 'a[rel="remove"]', function () {
    var tr = tblPedidos.cell($(this).closest('td, li')).index();
    pedidos.items.products.splice(tr.row, 1);
    pedidos.list();
}).on('change', 'input[name="cant"]', function () {
    console.clear();
    var cant = parseInt($(this).val());
    var tr = tblPedidos.cell($(this).closest('td, li')).index();
    pedidos.items.products[tr.row].cantidad = cant;
    pedidos.calc_invoice();
    $('td:eq(5)', tblPedidos.row(tr.row).node()).html('$' + pedidos.items.products[tr.row].subtotal.toFixed(2));
    console.log(cant);
});


// validar entrada
function validate_form_text(type, event, regex) {
    var key = event.keyCode || event.which;
    var numbers = (key > 47 && key < 58) || key === 8;
    var numbers_spaceless = (key > 47 && key < 58);
    var letters = !((key !== 32) && (key < 65) || (key > 90) && (key < 97) || (key > 122 && key !== 241 && key !== 209 && key !== 225 && key !== 233 && key !== 237 && key !== 243 && key !== 250 && key !== 193 && key !== 201 && key !== 205 && key !== 211 && key !== 218)) || key === 8;
    var letters_spaceless = !((key < 65) || (key > 90) && (key < 97) || (key > 122 && key !== 241 && key !== 209 && key !== 225 && key !== 233 && key !== 237 && key !== 243 && key !== 250 && key !== 193 && key !== 201 && key !== 205 && key !== 211 && key !== 218)) || key === 8;
    var decimals = ((key > 47 && key < 58) || key === 8 || key === 46);

    if (type === 'numbers') {
        return numbers;
    } else if (type === 'letters') {
        return letters;
    } else if (type === 'numbers_letters') {
        return numbers || letters;
    } else if (type === 'letters_spaceless') {
        return letters_spaceless;
    } else if (type === 'letters_numbers_spaceless') {
        return letters_spaceless || numbers_spaceless;
    } else if (type === 'decimals') {
        return decimals;
    } else if (type === 'regex') {
        return regex;
    }
    return true;
}