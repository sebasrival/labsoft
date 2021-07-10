// noinspection JSUnresolvedFunction,JSUnusedLocalSymbols

let tblCompra;

// Estructura para el detalle de pedidos
let factura_compra = {
    itemsFactura: {
        proveedor: '',
        nro_factura: '',
        timbrado: '',
        fecha_vencimiento_timbrado: '',
        fecha_vencimiento_credito: '',
        fecha_factura: '',
        tipo_compra: '',
        descuento: 0,
        totalIva10: 0.00,
        totalIva5: 0.00,
        total_compra: 0.00,
        metodo_pago: '',
        descripcion_pago: '',
        materias: []
    },
    calc_invoice: function () {
        let subtotal = 0.00;
        let iva10 = 0.00;
        let iva5 = 0.00;
        factura_compra.itemsFactura.descuento = $('#id_descuento').val();
        $.each(this.itemsFactura.materias, function (pos, dict) {
            dict.subtotal = dict.cantidad * dict.precio;
            subtotal += dict.subtotal;
            console.log(dict.iva);
            if (dict.iva === 10) {
                iva10 += dict.subtotal.toFixed(2) / 11
            } else if (dict.iva === 5) {
                iva5 += dict.subtotal.toFixed(2) / 21
            }
        });
        this.itemsFactura.total_compra = subtotal.toFixed(2);
        $('#total').val((this.itemsFactura.total_compra - ((this.itemsFactura.total_compra * this.itemsFactura.descuento) / 100)).toFixed(2));
        this.itemsFactura.totalIva10 = iva10.toFixed(2);
        this.itemsFactura.totalIva5 = iva5.toFixed(2);
        $('#totalIva5').val(iva5.toFixed(2));
        $('#totalIva10').val(iva10.toFixed(2));
    },
    add: function (item) {
        this.itemsFactura.materias.push(item);
        this.list();
    },
    list: function () {
        this.calc_invoice();
        tblCompra = $('#tFacturaCompra').DataTable({
            responsive: true,
            destroy: true,
            data: this.itemsFactura.materias,
            ordering: false,
            bAutoWidth: true,
            columns: [
                {"data": "codigo"},
                {"data": "nombre"},
                {"data": "precio"},
                {"data": "cantidad"},
                {"data": "iva"},
                {"data": "subtotal"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [2],
                    width: "20%",
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input name="ipPrecio" type="number" min="0" class="form-control form-control-sm"' +
                            ' value="' + data + '">';
                    }
                },
                {
                    targets: [4],
                    width: "11%",
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="number" name="ipIva" min="0" value="'+ row.iva + '" max="10" step="5" class="form-control form-control-sm input-sm">'
                    }
                },
                {
                    targets: [5],
                    class: "text-center",
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [3],
                    width: "13%",
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="number" name="ipCant"  min="1" value="'+ row.cantidad +'" class="form-control form-control-sm input-sm" autocomplete="off">';
                    }
                },
                {
                    targets: [6],
                    class: "text-center",
                    width: "5%",
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="btnRemove" class="btn btn-danger m-0 p-0"><i class="fa fa-trash m-1" aria-hidden="true"></i>\n</i></a>'
                    }
                }
            ]
        });
    }
};

$(function () {
    /**
     * Funcion para agregar Materia prima a detalle
     **/
    $('#frm-materia').click(function () {
        var materia = {};
        //obteniendo datos del modal
        materia['codigo'] = $('#id_codigo').val();
        materia['nombre'] = $('#id_nombre').val();
        materia['desc'] = $('#id_desc').val();
        materia['inci'] = $('#id_inci').val();
        materia['cantidadCont'] = $('#id_cantidadCont').val();
        materia['um'] = $('#id_um').val();

        console.log(materia);

        //validacion
        if (materia['codigo'] === "") {
            setTimeout(function () {
                $('#mdCodigo').html('Es necesario que complete el campo Codigo.');
            }, 300);
            $('#id_codigo').focus();
            return false;
        } else if (materia['nombre'] === "") {
            setTimeout(function () {
                $('#mdNombre').html('Es necesario que complete el campo Nombre.').fadeOut(3000);
            }, 300);
            $('#id_nombre').focus();
            return false;
        } else if (materia['cantidadCont'] === "" || materia['cantidadCont'] === "0") {
            setTimeout(function () {
                $('#mdCantidad').html('Es necesario que complete el campo Cantidad').fadeOut(3000);
            }, 300);
            $('#id_cantidadCont').focus();
            return false;
        } else if (materia['um'] === "") {
            setTimeout(function () {
                $('#mdUM').html('Es necesario que complete el campo Unidad de medida').fadeOut(3000);
            }, 300);
            $('#id_um').focus();
            return false;
        } else {
            //VALORES POR DEFECTO EN FORM MODAL
            materia['precio'] = 0;
            materia['iva'] = 10;
            materia['subtotal'] = 0;
            materia['cantidad'] = 1;
            materia['id'] = '';

            //validar si existe esa materia en el detalle
            let ban = false;
            $.each(factura_compra.itemsFactura.materias, function (key, value) {
                if (value.codigo === materia['codigo']) {
                    //cerrar modal
                    $('#materiaModal').modal('hide');
                    //limpiar form
                    $('#formMateria')[0].reset();
                    mensaje_error('Factura Detalle', 'Ya existe esta materia prima en el detalle.');
                    ban = true;
                }
            });
            if (!ban) {
                //se agrega los datos a la estructura
                factura_compra.add(materia)
            }
            //cerrar modal
            $('#materiaModal').modal('hide');
            //limpiar form
            $('#formMateria')[0].reset();
        }
    });

    $('#materia_select').on('select2:select', function (e) {
        let data = e.params.data;
        data['cantidad'] = 1;
        data['subtotal'] = 0.00;
        data['precio'] = 0 // se le agrega por ahora puede que en el modelo materia tenga precio
        data['iva'] = 10

        //validar si existe esa materia en el detalle
        let ban = false;
        $.each(factura_compra.itemsFactura.materias, function (key, value) {
            if (value.codigo === data['codigo']) {
                $('#materia_select').val('');
                mensaje_error('Factura Detalle', 'Ya existe esta materia prima en el detalle.');
                ban = true;
            }
        });

        if (!ban) {
            //se agrega los datos a la estructura
            factura_compra.add(data)
            // borra luego de la seleccion
        }
        $(this).val('').trigger('change.select2');
    });

    $('#btnDelete').on('click', function () {
        if (factura_compra.itemsFactura.materias.length === 0) return false;
        alert_delete_custom('Notificación', '¿Estás seguro de eliminar todos los detalles de compras', function () {
            factura_compra.itemsFactura.materias = []
            factura_compra.list();
        });
    });

    $('#id_descuento').on('change keyup paste ready', function () {
        if (factura_compra.itemsFactura.materias.length === 0) return false;
        factura_compra.calc_invoice();
    });

    $('#tFacturaCompra').on('click', 'a[rel="btnRemove"]', function () {
        let tr = tblCompra.cell($(this).closest('td, li')).index();
        factura_compra.itemsFactura.materias.splice(tr.row, 1);
        factura_compra.list();
    }).on('change keyup paste', 'input[name="ipCant"]', function () {
        let cant = parseInt($(this).val());
        let tr = tblCompra.cell($(this).closest('td, li')).index();
        factura_compra.itemsFactura.materias[tr.row].cantidad = cant;
        factura_compra.calc_invoice();
        $('td:eq(5)', tblCompra.row(tr.row).node()).html(factura_compra.itemsFactura.materias[tr.row].subtotal.toFixed(2));
    }).on('change keyup paste', 'input[name="ipPrecio"]', function () {
        let precio = parseFloat($(this).val());
        let tr = tblCompra.cell($(this).closest('td, li')).index();
        factura_compra.itemsFactura.materias[tr.row].precio = precio.toFixed(2);
        factura_compra.calc_invoice();
        $('td:eq(5)', tblCompra.row(tr.row).node()).html(factura_compra.itemsFactura.materias[tr.row].subtotal.toFixed(2));
    }).on('change', 'input[name="ipIva"]', function () {
        let iva = parseInt($(this).val());
        let tr = tblCompra.cell($(this).closest('td, li')).index();
        factura_compra.itemsFactura.materias[tr.row].iva = iva;
        factura_compra.calc_invoice();
        //preguntar si esto debe afectar el iva del subtotal
        //$('td:eq(5)', tblCompra.row(tr.row).node()).html('$' + factura_compra.itemsFactura.materias[tr.row].subtotal.toFixed(2));
    });

    $('form').on('submit', function (e) {
        e.preventDefault();
        if (factura_compra.itemsFactura.materias.length === 0) {
            mensaje_error('Error para Registrar', 'Debe por lo menos tener un detalle para guardar.');
            return false;
        }
        factura_compra.itemsFactura.proveedor = $('#proveedor_select').val();
        factura_compra.itemsFactura.nro_factura = $('#id_nro_factura').val();
        factura_compra.itemsFactura.tipo_compra = $('input:radio[name="tipo_factura"]:checked').val();
        factura_compra.itemsFactura.fecha_factura = $('#id_fecha_factura').val();
        factura_compra.itemsFactura.timbrado = $('#id_timbrado').val();
        factura_compra.itemsFactura.fecha_vencimiento_credito = $('#id_fecha_vencimiento_credito').val();
        factura_compra.itemsFactura.fecha_vencimiento_timbrado = $('#id_fecha_vencimiento_timbrado').val();
        factura_compra.itemsFactura.metodo_pago = $('#id_metodo_pago').val();
        factura_compra.itemsFactura.descripcion_pago = $('#descripcion_pago').val();
        console.log(factura_compra.itemsFactura.fecha_factura);
        let parameters = new FormData();
        parameters.append('factura_compra', JSON.stringify(factura_compra.itemsFactura));
        let csrf = $('input[name="csrfmiddlewaretoken"]').val();
        console.log(csrf);
        parameters.append('csrfmiddlewaretoken', csrf);
        console.log(factura_compra.itemsFactura);
        create_ajax_factura(window.location.pathname, 'JSON', parameters, '/modulos/compras/factura/list/');
    });
});