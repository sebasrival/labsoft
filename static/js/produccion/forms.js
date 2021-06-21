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
        cantidad_teorica: 0

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
        this.items.producto=this.items.materias[0].producto_id;
        $('input[name="producto"]').val(this.items.materias[0].producto)
        this.items.estado=$('select[name="estado"]').val();
        this.listEquipo();
        if (this.items.estado=='EN PRODUCCION'){
            $('input[name="fecha_emision"]').attr('disabled',true);
            $('input[name="elaborado_por"]').attr('disabled',true);
            $('input[name="producto"]').attr('disabled',true);
            $('input[name="cantidad_teorica"]').attr('disabled',true);
            $('input[name="cant"]').attr('disabled',true);
            $( 'a[rel="remove"]').hide();
            $('.btnRemoveAll').attr('disabled',true);
            $('#search').attr('disabled',true);
        }
        if (this.items.estado=='FINALIZADA'){
            $('input[name="fecha_emision"]').attr('disabled',true);
            $('input[name="producto"]').attr('disabled',true);
            $('input[name="cantidad_teorica"]').attr('disabled',true);
            $('input[name="cant"]').attr('disabled',true);
            $( 'a[rel="remove"]').hide();
            $('.btnRemoveAll').attr('disabled',true);
            $('#search').attr('disabled',true);
            $('#searchEquipo').attr('disabled',true);
            $('input[name="aprobado_por"]').attr('disabled',true);
            $('select[name="estado"]').attr('disabled',true);
            $('input[name="verificado_por"]').attr('disabled',true);
            $('input[name="elaborado_por"]').attr('disabled',true);
            $('input[name="fecha_vigencia"]').attr('disabled',true);
            $( 'a[rel="removeEquipo"]').hide();
            $('input[name="descripcion_modificacion"]').attr('disabled',true);
            $('.btnRemoveAllEquipo').attr('disabled',true);

        }
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
                {"data": "id11"},
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
            if (ui.item.materias!=undefined){
                orden.items.materias=ui.item.materias;
            }
            else{
                orden.items.materias=[];
            }
            orden.items.producto=ui.item.id;
            console.log(ui.item.materias);
            orden.list();
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
        estado_nuevo=$('select[name="estado"]').val();
        console.log(estado_nuevo);
        console.log(orden.items.estado);

        if ((orden.items.estado=='EN PRODUCCION'|| orden.items.estado=='FINALIZADA') && estado_nuevo=='PENDIENTE'){
            show_notify_error('No puede cambiar el estado de '+orden.items.estado +' a PENDIENTE.');
            return false;
        }
        if (orden.items.estado=='FINALIZADA' && (estado_nuevo=='PENDIENTE' || estado_nuevo=='EN PRODUCCION')){
            show_notify_error('No puede cambiar el estado de '+orden.items.estado +' a '+estado_nuevo);
            return false;
        }
        orden.items.fecha_emision = $('input[name="fecha_emision"]').val();
        orden.items.fecha_vigencia = $('input[name="fecha_vigencia"]').val();
        orden.items.elaborado_por = $('input[name="elaborado_por"]').val();
        orden.items.aprobado_por = $('input[name="aprobado_por"]').val();
        orden.items.verificado_por = $('input[name="verificado_por"]').val();
        orden.items.estado = $('select[name="estado"]').val();
        orden.items.descripcion_modificacion = $('input[name="descripcion_modificacion"]').val();
        orden.items.cantidad_teorica = $('input[name="cantidad_teorica"]').val();
        if(orden.items.materias.length === 0){
            mensaje_error('Debe al menos tener una materia prima en su orden.');
            return false;
        }
        if(orden.items.fecha_emision>orden.items.fecha_vigencia){
            show_notify_error('La fecha de vigencia no puede ser menor a la fecha de emision.')
            return false;
        }
        



        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('orden', JSON.stringify(orden.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/modulos/produccion/orden/list/';
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