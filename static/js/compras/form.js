var tblCompra;

// Estructura para el detalle de pedidos
var factura_compra = {
    itemsFactura: {
        proveedor: '',
        nro_factura: '',
        fecha_factura: '',
        tipo_compra: '',
        descuento: 0,
        totalIva10: 0,
        totalIva5: 0,
        exenta: 0,
        total_compra:0,
        materias: []
    },
    calc_invoice: function () {
        var subtotal = 0.00
        $.each(this.itemsFactura.materias, function (pos, dict) {
            dict.subtotal = dict.cantidad * parseFloat(dict.precio);
            subtotal += dict.subtotal;
        });
        this.itemsFactura.total_compra = subtotal;
        $('#total').val(this.itemsFactura.total_compra.toFixed(2));
    },
    add: function (item) {
        this.itemsFactura.materias.push(item);
        this.list();
    },
    list: function () {
        //this.calc_invoice()
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
                        return '<input id="ipPrecio" type="number" min="1" class="form-control form-control-sm">'
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
                        return '<a rel="remove" class="btn btn-danger m-0 p-0"><i class="fa fa-trash m-1" aria-hidden="true"></i>\n</i></a>'
                    }
                }
            ]
        });
    }
}

$(function () {
    /*
    * Funcion para agregar Materia prima a detalle
    * */
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
                $('#mdNombre').html('Es necesario que complete el campo Nombre.');
            }, 300);
            $('#id_nombre').focus();
            return false;
        }
        else if (materia['cantidadCont'] === "" || materia['cantidadCont'] === "0"){
            setTimeout(function (){
                $('#mdCantidad').html('Es necesario que complete el campo Cantidad');
            }, 300);
            $('#id_cantidadCont').focus();
            return false;
        }else if (materia['um'] === ""){
            setTimeout(function (){
                $('#mdUM').html('Es necesario que complete el campo Unidad de medida');
            }, 300);
            $('#id_um').focus();
            return false;
        }else{
            materia['precio'] = 0;
            materia['iva'] = 0;
            materia['exenta'] = 0;
            materia['subtotal'] = 0;
            materia['cantidad'] = 0;
            materia['id'] = '';

            factura_compra.add(materia);
        }
        console.log(materia);
    });
});