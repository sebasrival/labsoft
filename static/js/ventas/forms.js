var tblFactura;

// Estructura para el detalle de facturas
var factura = {
    items: {
        cliente: '',
        nro_factura: '',
        //fecha_pedido: '',
        fecha_emision: '',
        total_iva: 0,
        total_factura: 0,
        products: []
    },
    calc_invoice: function () {
        var subtotal = 0
        $.each(this.items.products, function (pos, dict) {
            dict.subtotal = dict.cantidad * parseFloat(dict.precio);
            subtotal += dict.subtotal;
        })
        this.items.total_factura = Math.round(subtotal);
        this.items.total_iva = Math.round(subtotal/11);
        $('#totalIva').val(this.items.total_iva); // el iva en el template
        $('#total').val(this.items.total_factura); // para el total
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        this.calc_invoice()
        tblFactura = $('#tblFactura').DataTable({
            responsive: true,
            destroy: true,
            data: this.items.products,
            ordering: false,
            columns: [
                {"data": "codigo_producto"},
                {"data": "description"},
                {"data": "precio"},
                {"data": "cantidad"},
                {"data": "subtotal"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: "text-center",
                    width: "10%",
                    orderable: false,
                },
                {
                    targets: [1],
                    class: "",
                    width: "30%",
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="descripcion" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.nombre + '">';
                    }
                },
                {
                    targets: [2, 4],
                    class: "text-center my-0 ",
                    orderable: false,
                    render: function (data, type, row) {
                        return 'Gs. ' + parseFloat(data);
                    }
                },
                {
                    targets: [3],
                    width: "20%",
                    class: "text-center",
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
                    }
                },
                {
                    targets: [5],
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

$(function () {
    $('#search').on('select2:select', function (e) {
        var data = e.params.data;
        data['cantidad'] = 1;
        //data['subtotal'] = 0;
        //se agrega los datos a la estructura
        factura.add(data)
        // borra luego de la seleccion
        $(this).val('').trigger('change.select2');
    });

    $('.btnRemoveAll').on('click', function () {
        if (factura.items.products.length === 0) return false;
        alert_delete('Notificación', '¿Estás seguro de eliminar todos los detalles de la factura', function () {
            factura.items.products = [];
            factura.list();
        });
    });

    $('#tblFactura').on('click', 'a[rel="remove"]', function () {
        var tr = tblFactura.cell($(this).closest('td, li')).index();
        factura.items.products.splice(tr.row, 1);
        factura.list();
    }).on('change', 'input[name="cant"]', function () {
        console.clear();
        var cant = parseInt($(this).val());
        var tr = tblFactura.cell($(this).closest('td, li')).index();
        factura.items.products[tr.row].cantidad = cant;
        factura.calc_invoice();
        // el 4 es el lugar donde tiene que estar el subtotal
        $('td:eq(4)', tblFactura.row(tr.row).node()).html('Gs.' + Math.round(factura.items.products[tr.row].subtotal));
        console.log(cant);
    }).on('change', 'input[name="descripcion"]', function (){
        var descripcion = $(this).val();
        var tr = tblFactura.cell($(this).closest('td, li')).index();
        factura.items.products[tr.row].description = descripcion;
    });

    $('form').on('submit', function (e) {
        e.preventDefault();
        factura.items.cliente = $('select[name="cliente"]').val();
        console.log('Cliente: ' + factura.items.cliente);
        factura.items.fecha_emision = $('input[name="fecha_emision"]').val();
        console.log('Fecha emision: ' + factura.items.fecha_emision);
        factura.items.nro_factura = $('input[name="nro_factura"]').val();
        console.log('prueba fac ' + factura.items.nro_factura);
        var parameters = new FormData();
        parameters.append('factura', JSON.stringify(factura.items));
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        console.log(csrf);
        parameters.append('csrfmiddlewaretoken', csrf);
        console.log(factura.items);
        submit_with_ajax(window.location.pathname, 'Noticicación', '¿Desea registrar esta factura?', parameters, function () {
            location.href = "/factura/list"
        });
    });
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