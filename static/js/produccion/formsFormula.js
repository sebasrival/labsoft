var tblOrden;
var tblEquipo;

// Estructura para el detalle de facturas
var orden = {
    items: {
        fecha_emision: '',
        materias: [],
        equipos: [],
        producto: '',
        elaborado_por: '',
        verificado_por: '',
        aprobado_por : '',
        fecha_vigencia: '',
        descripcion_modificacion:'',
        estado: '',
        numero:'',
        cantidad_teorica: 0,
        check: 0

    },
    add: function (item) {
        this.items.materias.push(item);
        this.list();
    },
    addEquipo: function (item) {
        this.items.equipos.push(item);
        this.listEquipo();
    },

    setOrdenEdit: function () {
        this.items.check=1;

        this.items.producto=this.items.materias[0].producto_id;
        var unidad_medida=this.items.materias[0].unidad_medida_producto;
        console.log(this.items.materias[0].unidad_medida_producto);
        if (unidad_medida =='GRAMOS'){
            $('#unidad_medida').val('Kilogramos');
        }
        else{
            $('#unidad_medida').val('Litros');
        }
      
        $('input[name="producto"]').val(this.items.materias[0].producto);
        $('input[name="cantidad_teorica"]').val(this.items.materias[0].cantidad_teorica);

    },
    list: function () {
        tblOrden = $('#tblOrden').DataTable({
            responsive: true,
            destroy: true,
            data: this.items.materias,
            ordering: false,
            columns: [
                {"data": "codigo"},
                {"data": "description"},
                {"data": "inci"},
                {"data": "cantidad"},
                {"data": "unidad_medida"},
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
                        return '<input type="text" name="descripcion" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.descripcion + '">';
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
                    targets: [5],
                    class: "text-center",
                    width: "5%",
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger m-0 p-0"><i class="fa fa-trash m-1" aria-hidden="true"></i>\n</i></a>'
                    }
                },
            ],
         
        });
    },
    listEquipo: function () {
        tblEquipo = $('#tblEquipo').DataTable({
            responsive: true,
            destroy: true,
            data: this.items.equipos,
            ordering: false,
            columns: [
                {"data": "codigo"},
                {"data": "descripcion"},
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
                        return '<input type="" name="descripcion" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.descripcion + '">';
                    }
                },
                {
                    targets: [2],
                    class: "text-center",
                    width: "5%",
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="removeEquipo" class="btn btn-danger m-0 p-0"><i class="fa fa-trash m-1" aria-hidden="true"></i>\n</i></a>'
                    }
                },
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
                    'action': 'search_materias',
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
            ui.item.cantidad = 1;
            console.log(orden.items);
            orden.add(ui.item);
            $(this).val('');
        }
    });

    $('#searchEquipo').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_equipos',
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
            orden.addEquipo(ui.item);
            $(this).val('');
        }
    });
    
    $('input[name="producto"]').autocomplete({
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
            console.log(ui.item.materias);
            orden.items.objecto_producto=ui.item;
            if (orden.items.objecto_producto.unidad_medida== 'MILILITROS'){
                $('#unidad_medida').val('Litros');
            }
            else{
                $('#unidad_medida').val('Kilogramos');

            }
            orden.items.producto=ui.item.id;
            //console.log(ui.item.materias);
           /* orden.list();*/
            $(this).val(ui.item.nombre);
            
        }
    });

    $('.btnRemoveAll').on('click', function () {
        if (orden.items.materias.length === 0) return false;
        alert_delete('Notificación', '¿Estás seguro de eliminar todos los detalles de la orden', function () {
            orden.items.materias = [];
            orden.list();
        });
    });

    $('.btnFormula').on('click', function (request, response) {
        if ( $('input[name="producto"]').val()==''|| $('input[name="cantidad_teorica"]').val()==''){
            show_notify_error('Debe especificar el producto y la cantidad teorica. ')
            return false;
        }
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_formula',
                'term': orden.items.producto,
                'cantidad': $('input[name="cantidad_teorica"]').val(),
            },
            dataType: 'json',
        }).done(function (data) {
            console.log(data);
            if (data.length==0){
              show_notify_success('No existe formula para este producto. Puede agregarlo.!');
              orden.items.check=1;
            }
            else {
               orden.items.check=-1;
               show_notify_error('Ya se añadio la formula para este producto.');
               
            }
          
            
        }).fail(function (jqXHR, textStatus, errorThrown) {
            //alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    },);


    $('#tblOrden').on('click', 'a[rel="remove"]', function () {
        var tr = tblOrden.cell($(this).closest('td, li')).index();
        orden.items.materias.splice(tr.row, 1);
        orden.list();
    }).on('change', 'input[name="cant"]', function () {
        console.clear();
        var cant = $(this).val();
        console.log(cant);
        var tr = tblOrden.cell($(this).closest('td, li')).index();
        orden.items.materias[tr.row].cantidad = cant;
    });
  
    $('.btnRemoveAllEquipo').on('click', function () {
        if (orden.items.materias.length === 0) return false;
        alert_delete('Notificación', '¿Estás seguro de eliminar todos los equipos de la orden', function () {
            orden.items.equipos = [];
            orden.listEquipo();
        });
    });

    $('#tblEquipo').on('click', 'a[rel="removeEquipo"]', function () {
        var tr = tblEquipo.cell($(this).closest('td, li')).index();
        orden.items.equipos.splice(tr.row, 1);
        orden.listEquipo();
    });
    $('form').on('submit', function (e) {
        e.preventDefault();
        if(orden.items.check==0){
            show_notify_error('Debe verificar la existencia de la formula para poder agregarla. ');
            return false;
        }
        if(orden.items.check==-1){
            show_notify_error('La formula para este producto y cantidad teorica ya existe.');
            return false;
        }
        if ($('input[name="cantidad_teorica"]').val()==0 || $('input[name="producto"]').val()==''){
            show_notify_error('Debe completar todos los datos. ');
            return false;
        }
        orden.items.cantidad_teorica=$('input[name="cantidad_teorica"]').val();
        if(orden.items.materias.length === 0){
            mensaje_error('Debe al menos tener una materia prima en su formula.');
            return false;
        }
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('orden', JSON.stringify(orden.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/modulos/produccion/formula/list/';
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