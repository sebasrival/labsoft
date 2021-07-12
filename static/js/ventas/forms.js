var tblFactura;
var tblCobro;

// Estructura para el detalle de facturas
var factura = {
    items: {
        cliente: '',
        nro_factura: '',
        fecha_emision: '',
        total_iva10: 0,
        total_iva5: 0,
        tipo_venta:'',
        subtotal: 0,
        total_factura:0,
        cobro:'',
        metodo_cobro:'',
        tipo_cobro: '',
        cuotas:[],
        datos_pedido:'',
        cant_cuotas:0,
        productos: [],
        cliente_razon_social:'',
        cliente_ruc:'',
        cobro_edit: 0,

    },
    itemCobro: {
        nro_cuota: 0,
        estado:'',
        monto: '',
        fecha_vencimiento: '',
    },
    calc_invoice: function () {
        var subtotal = 0
        var iva5=0
        var iva10=0
        var exenta=0
        $.each(this.items.productos, function (pos, dict) {
            dict.subtotal = dict.cantidad * parseFloat(dict.precio);
            subtotal += dict.subtotal;
            if (dict.tasa_iva==5){
                iva5 += Math.round(dict.subtotal/21);
            }else if (dict.tasa_iva==10) {
                iva10 += Math.round(dict.subtotal/11);
            }
            else{
                exenta +=dict.subtotal;
            }
            dict.subtotal = dict.cantidad * parseFloat(dict.precio);

        })

        this.items.total_factura = Math.round(subtotal);
        this.items.total_iva5 = Math.round(iva5);
        this.items.total_iva10 = Math.round(iva10);
        this.items.total_exenta=Math.round(exenta);

        $('#totalIva10').val(this.items.total_iva10); // el iva en el template
        $('#totalIva5').val(this.items.total_iva5); // el iva en el template
        $('#totalExenta').val(this.items.total_exenta); // el iva en el template

        $('#total').val(this.items.total_factura); // para el total
    },
    add: function (item) {
        this.items.productos.push(item);
        this.list();
    },

    setCobroEdit: function () {
        $('#botonCobro').hide();
        console.log(factura.items.cuotas[0].tipo_cobro);
        $('#tipoCobro').val(factura.items.cuotas[0].tipo_cobro);
        $('#cuotas').val(factura.items.cuotas[0].cantidad_cuotas);
        $('#medioCobro').val(factura.items.cuotas[0].medio_cobro);
        $('#razonSocial').val(factura.items.cuotas[0].razon_social);
        $('input[name="cliente"]').val(factura.items.cuotas[0].ruc);
        factura.items.cliente=factura.items.cuotas[0].cliente_id;

    },
    setDatosPedido: function () {
        $('#razonSocial').val(factura.items.datos_pedido[0].cliente);
        $('input[name="cliente"]').val(factura.items.datos_pedido[0].cliente_ruc);
        factura.items.cliente=factura.items.datos_pedido[0].cliente_id;

    },
    
    
    addCobro: function(){
        factura.items.cant_cuotas = $('#cuotas').val();
        factura.items.tipo_cobro=$('#tipoCobro').val();
        var today = new Date();
        var vencimiento=new Date();
     
        var i;
        if (factura.items.tipo_cobro=='Credito'){
                var datosCobro ={
                    cantidad_cuotas: 0,
                    estado:'',
                    monto: '',
                    fecha: '',
                    tipo_cobro:'',
                    medio_cobro:'',
                };
                datosCobro.cantidad_cuotas=factura.items.cant_cuotas;
                datosCobro.estado='PENDIENTE';
                datosCobro.monto=  $('#total').val();
                datosCobro.fecha=vencimiento.toISOString().split('T')[0];
                vencimiento.setDate(vencimiento.getDate() + (30 * factura.items.cant_cuotas ));
                datosCobro.fecha_vencimiento=vencimiento.toISOString().split('T')[0];
                datosCobro.medio_cobro='N/A';
                datosCobro.tipo_cobro=factura.items.tipo_cobro;
                factura.items.metodo_cobro="N/A";
                factura.items.cuotas.push(datosCobro);
                this.listCobro();
        }
        else{
            var datosCobro ={
                cantidad_cuotas: 0,
                estado:'',
                monto: '',
                fecha: '',
                tipo_cobro:'',
                medio_cobro:'',
                fecha_vencimiento: 'N/A'
                
            };
            datosCobro.cantidad_cuotas=0;
            datosCobro.estado='PAGADA';
            datosCobro.monto=  $('#total').val();
            datosCobro.fecha=today.toISOString().split('T')[0];
            datosCobro.medio_cobro=$('#medioCobro').val();
            factura.items.metodo_cobro=$('#medioCobro').val();
            datosCobro.tipo_cobro=factura.items.tipo_cobro;
            factura.items.cuotas.push(datosCobro);
            this.listCobro();

        }

    },
    getDatosCobro: function () {
        $('#razonSocial').val(item.razon_social);
    },
    setDatosCliente: function (item) {
        $('#razonSocial').val(item.razon_social);
    },
    setCuota: function (cant) {
        $('#cuotas').val(cant);

    },
    list: function () {
        this.calc_invoice()
        tblFactura = $('#tblFactura').DataTable({
            responsive: true,
            destroy: true,
            data: this.items.productos,
            ordering: false,
            columns: [
                {"data": "codigo_producto"},
                {"data": "description"},
                {"data": "precio"},
                {"data": "cantidad"},
                {"data": "tasa_iva"},
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
                    targets: [2, 5],
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
                        return '<input type="text" name="cant"  class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
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
                    min: 1,
                    max: parseInt(data.cantidad_stock),
                    step: 1,
                    boostat: 5,
                    maxboostedstep: 10,
                }).keypress(function (e) {
                    return validate_form_text('numbers', e, null);
                });
            },
        });
    },
    listCobro: function () {
        tblCobro = $('#tblCobro').DataTable({
            responsive: true,
            destroy: true,
            data: factura.items.cuotas,
            ordering: false,
            columns: [
                {"data": "tipo_cobro"},
                {"data": "monto"},
                {"data": "medio_cobro"},
                {"data": "estado"},
                {"data": "cantidad_cuotas"},
                {"data": "fecha"},
                {"data": "fecha_vencimiento"},

            ],
 
        });
    },



}

$(function () {
    

    $('#search').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();

            console.log (ui.item.cantidad_stock);
            if (ui.item.cantidad_stock ==0){
                show_notify_error('El producto seleccionado no posee stock disponible. ');
            }
            else{
                ui.item.cantidad = 1;
                ui.item.subtotal = 0.00;
                console.log(ui.item);
                factura.add(ui.item);
                $(this).val('');
            }
        }
    });
    
    $('input[name="cliente"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_clientes',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            factura.items.cliente=ui.item.id
            console.log(factura.items);
            $(this).val(ui.item.ruc);
            factura.setDatosCliente(ui.item);
            
        }
    });
    $('#tipoCobro').on('change', function (e) {
        var tipocobro=$('#tipoCobro').val()

        if (tipocobro=='Contado'){
            factura.setCuota(0);
            $('#medioCobro').attr('disabled', false);
            $('#cuotas').attr('disabled', true);

        }
        else{
            $('#medioCobro').val('');
            factura.setCuota(2);
            $('#medioCobro').attr('disabled', true);
            $('#cuotas').attr('disabled', false);

        }
        console.log(tipocobro)
    });
    $('#puntoVenta').on('change', function (e) {
        var punto=$('#puntoVenta').val();
        if (punto!='') {
        console.log(punto);
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'set_punto_venta',
                'term': punto,
            },
            dataType: 'json',
        }).done(function (data) {
            var numero=data[0].numeracion_actual;
            var string=numero.toString();
            var nro;
            console.log(data[0].numeracion_actual.length);
            if (string.length==1){
                nro='000000' +data[0].numeracion_actual;
            }
            if (string.length==2){
                nro='00000' +data[0].numeracion_actual;
            }
            if (string.length==3){
                nro='0000' +data[0].numeracion_actual;
            }
            if (string.length==4){
                nro='000' +data[0].numeracion_actual;
            }
            if (string.length==5){
                nro='00' +data[0].numeracion_actual;
            }
            if (string.length==6){
                nro='0' +data[0].numeracion_actual;
            }
            if (string.length==7){
                nro=data[0].numeracion_actual;
            }
            $('input[name="nro_factura"]').val(''+data[0].sucursal+'-'+data[0].punto_venta+'-'+nro);
            factura.items.numeracion_actual = data[0].numeracion_actual;
            factura.items.punto_venta = data[0].punto_venta;
            factura.items.sucursal=data[0].sucursal;

            console.log(data[0].numeracion_actual);  

            
        }).fail(function (jqXHR, textStatus, errorThrown) {
            //alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    }
    else{
        $('input[name="nro_factura"]').val('');
    }
       
    });
    $('#botonCobro').on('click', function (e) {
        var estado= $('#botonCobro').disabled;
        console.log(estado);
        if(factura.items.total_factura === 0){
            alert('Debe especificar los datos de la factura primero');
            return false;
        }
        else{
            factura.addCobro();
        }
        $('#botonCobro').hide();
    }
    )

    $('.btnRemoveAll').on('click', function () {
        if (factura.items.productos.length === 0) return false;
        alert_delete('Notificación', '¿Estás seguro de eliminar todos los detalles de la factura', function () {
            factura.items.productos = [];
            factura.list();
        });
    });
    $('.btnRemoveAllCobro').on('click', function () {
        if (factura.items.cuotas.length === 0) return false;
        alert_delete('Notificación', '¿Estás seguro de eliminar todos los detalles del cobro', function () {
            factura.items.cuotas = [];
            factura.listCobro();
            factura.items.cobro_edit=1;
        });
        $('#botonCobro').show();


    });
    $('#tblFactura').on('click', 'a[rel="remove"]', function () {
        var tr = tblFactura.cell($(this).closest('td, li')).index();
        factura.items.productos.splice(tr.row, 1);
        factura.list();
    }).on('change', 'input[name="cant"]', function () {
        console.clear();
        var cant = parseInt($(this).val());
        console.log(cant);
        var tr = tblFactura.cell($(this).closest('td, li')).index();
        factura.items.productos[tr.row].cantidad = cant;
        factura.calc_invoice();
        // el 4 es el lugar donde tiene que estar el subtotal
        $('td:eq(5)', tblFactura.row(tr.row).node()).html('Gs.' + Math.round(factura.items.productos[tr.row].subtotal));
        console.log(cant);
    }).on('change', 'input[name="descripcion"]', function (){
        var descripcion = $(this).val();
        var tr = tblFactura.cell($(this).closest('td, li')).index();
        factura.items.products[tr.row].description = descripcion;
    });

    $('form').on('submit', function (e) {
        e.preventDefault();

        if(factura.items.productos.length === 0){
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }
        if(factura.items.cuotas.length === 0){
            message_error('Debe especificar los datos del cobro.');
            return false;
        }

        factura.items.fecha_emision = $('input[name="fecha_emision"]').val();
        factura.items.nro_factura = $('input[name="nro_factura"]').val();
        factura.items.metodo_cobro=$('#medioCobro').val();
        factura.items.cant_cuotas = $('#cuotas').val();
        factura.items.tipo_cobro=$('#tipoCobro').val();

        if (factura.items.cliente==''){
            factura.items.cliente_razon_social=$('#razonSocial').val();
            factura.items.cliente_ruc=$('input[name="cliente"]').val();
            
        }
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('factura', JSON.stringify(factura.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/modulos/ventas/facturas/list/';
        });
    });

    $('#fecha_emision').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
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
function datosCobro() {
    return {
      'userID':   '',
      'email':    '',
      'name':     '',
      'stage':    '',
      'poster':   false,
      'canEmail': false,
      'stage':    ''
    };
  };