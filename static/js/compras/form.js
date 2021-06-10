var tblCompra;

// Estructura para el detalle de pedidos
var factura_compra = {
    itemsFactura: {
        proveedor: '',
        nro_factura: '',
        fecha_factura: '',
        tipo_compra: '',
        descuento: 0,
        totalIva10: 0.00,
        totalIva5: 0.00,
        exenta: 0.00,
        total_compra:0.00,
        materias: []
    },
    calc_invoice: function () {
        var subtotal = 0.00;
        var iva10 = 0.00;
        var iva5 = 0.00;
        $.each(this.itemsFactura.materias, function (pos, dict) {
            dict.subtotal = dict.cantidad * dict.precio;
            subtotal += dict.subtotal;

            if(dict.iva === 10){
                iva10 += dict.subtotal.toFixed(2) / 11
            }else if(dict.iva === 5){
                iva5 += dict.subtotal.toFixed(2) / 21
            }
        });
        this.itemsFactura.total_compra = subtotal.toFixed(2);
        $('#total').val((this.itemsFactura.total_compra - ((this.itemsFactura.total_compra * this.itemsFactura.descuento) / 100)).toFixed(2));
        this.itemsFactura.totalIva10 = iva10;
        this.itemsFactura.totalIva5 = iva5;
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
                        return '<input id="ipPrecio" type="number" min="0" step="1000" class="form-control form-control-sm"' +
                            ' value="'+ data + '">';
                    }
                },
                {
                  targets: [4],
                  width: "11%",
                  class: 'text-center',
                  render: function (data, type, row) {
                        return '<input type="number" id="ipIva" min="0" value="10" max="10" step="5" class="form-control form-control-sm input-sm">'
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
                        return '<input type="number" id="ipCant"  min="1" value="1" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
                    }
                },
                {
                    targets: [6],
                    class: "text-center",
                    width: "5%",
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a id="btnRemove" class="btn btn-danger m-0 p-0"><i class="fa fa-trash m-1" aria-hidden="true"></i>\n</i></a>'
                    }
                }
            ]
        });
    }
}

$(function () {
    /**
     * Funcion para agregar Materia prima a detalle
     **/
    $('#frm-materia').click(function (){
        materia = {};
        //obteniendo datos del modal
        materia['codigo'] = $('#id_codigo').val();
        materia['nombre'] = $('#id_nombre').val();
        materia['descripcion'] = $('#id_descripcion').val();
        materia['inci'] = $('#id_inci').val();
        materia['cantidadCont'] = $('#id_cantidadCont').val();
        materia['um'] = $('#id_um').val();

        //validacion
        if (materia['codigo'] === ""){
            setTimeout(function (){
                $('#mdCodigo').html('Es necesario que complete el campo Codigo.');
            }, 300);
            $('#id_codigo').focus();
            return false;
        }else if (materia['nombre'] === ""){
            setTimeout(function (){
                $('#mdNombre').html('Es necesario que complete el campo Nombre.').fadeOut(3000);
            }, 300);
            $('#id_nombre').focus();
            return false;
        }
        else if (materia['cantidadCont'] === "" || materia['cantidadCont'] === "0"){
            setTimeout(function (){
                $('#mdCantidad').html('Es necesario que complete el campo Cantidad').fadeOut(3000);
            }, 300);
            $('#id_cantidadCont').focus();
            return false;
        }else if (materia['um'] === ""){
            setTimeout(function (){
                $('#mdUM').html('Es necesario que complete el campo Unidad de medida').fadeOut(3000);
            }, 300);
            $('#id_um').focus();
            return false;
        }else{
            //VALORES POR DEFECTO EN FORM MODAL
            materia['precio'] = 0;
            materia['iva'] = 10;
            materia['subtotal'] = 0;
            materia['cantidad'] = 1;
            materia['id'] = '';
            factura_compra.add(materia);
            //cerrar modal
            $('#materiaModal').modal('hide');
            //limpiar form
            $('#formMateria')[0].reset();
        }
        console.log(materia);
    });

    $('#materia_select').on('select2:select', function (e) {
        var data = e.params.data;
        data['cantidad'] = 1;
        data['subtotal'] = 0.00;
        data['precio'] = 0 // se le agrega por ahora puede que en el modelo materia tenga precio
        data['iva'] = 10
        //se agrega los datos a la estructura
        factura_compra.add(data)
        // borra luego de la seleccion
        $(this).val('').trigger('change.select2');
    });

    $('#btnDelete').on('click', function () {
        if (factura_compra.itemsFactura.materias.length === 0) return false;
        alert_delete_custom('Notificación', '¿Estás seguro de eliminar todos los detalles de compras', function () {
            factura_compra.itemsFactura.materias = []
            factura_compra.list();
        });
    });

    $('#id_descuento').on('change keyup paste', function () {
        if (factura_compra.itemsFactura.materias.length === 0) return false;
        factura_compra.itemsFactura.descuento = $(this).val();
        factura_compra.calc_invoice();
    });


    $('#tFacturaCompra').on('click', '#btnRemove', function () {
        var tr = tblCompra.cell($(this).closest('td, li')).index();
        factura_compra.itemsFactura.materias.splice(tr.row, 1);
        factura_compra.list();
    }).on('change keyup paste', '#ipCant', function () {
        var cant = parseInt($(this).val());
        var tr = tblCompra.cell($(this).closest('td, li')).index();
        factura_compra.itemsFactura.materias[tr.row].cantidad = cant;
        factura_compra.calc_invoice();
        $('td:eq(5)', tblCompra.row(tr.row).node()).html('$' + factura_compra.itemsFactura.materias[tr.row].subtotal);
    }).on('change keyup paste', '#ipPrecio', function () {
        var precio = parseFloat($(this).val());
        console.log(precio);
        var tr = tblCompra.cell($(this).closest('td, li')).index();
        factura_compra.itemsFactura.materias[tr.row].precio = precio.toFixed(2);
        factura_compra.calc_invoice();
        $('td:eq(5)', tblCompra.row(tr.row).node()).html('$' + factura_compra.itemsFactura.materias[tr.row].subtotal);
    }).on('change', '#ipIva', function () {
        var iva = parseInt($(this).val());
        var tr = tblCompra.cell($(this).closest('td, li')).index();
        factura_compra.itemsFactura.materias[tr.row].iva = iva;
        console.log(iva)
        factura_compra.calc_invoice();
        //preguntar si esto debe afectar el iva del subtotal
        //$('td:eq(5)', tblCompra.row(tr.row).node()).html('$' + factura_compra.itemsFactura.materias[tr.row].subtotal.toFixed(2));
    });
});