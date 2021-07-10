$('.btnReporteVenta').on('click', function() {
    console.log($('#anho').val())
    
    var anho= $('#anho').val()
    location.href = '/modulos/reportes/ventas/reporteventas/pdf/'+anho+'/';
});
$('.btnReporteVentaMensual').on('click', function() {
    console.log($('#mes').val())
    var anho= $('#anho').val()
    var mes= $('#mes').val()
    location.href = '/modulos/reportes/ventas/reporteventas/pdf/'+anho+'/'+mes+'/';
});
$('.btnReporteProductoMensual').on('click', function() {
    console.log($('#mes').val())
    var anho= $('#anho').val()
    var mes= $('#mes').val()
    location.href = '/modulos/reportes/produccion/reporteproductos/pdf/'+anho+'/'+mes+'/';
    
});

$('.btnReporteOrden').on('click', function() {
    console.log($('#mes').val())
    var inicio= $('#start').val()
    var final= $('#end').val()
    var estado= $('#estado').val()
    location.href = '/modulos/reportes/produccion/reporteorden/pdf/'+inicio+'/'+final+'/'+estado+'/';
    
});