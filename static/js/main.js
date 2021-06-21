(function () {
    "use strict";

    var treeviewMenu = $('.app-menu');

    // Toggle Sidebar
    $('[data-toggle="sidebar"]').click(function (event) {
        event.preventDefault();
        $('.app').toggleClass('sidenav-toggled');
    });

    // Activate sidebar treeview toggle
    $("[data-toggle='treeview']").click(function (event) {
        event.preventDefault();
        if (!$(this).parent().hasClass('is-expanded')) {
            treeviewMenu.find("[data-toggle='treeview']").parent().removeClass('is-expanded');
        }
        $(this).parent().toggleClass('is-expanded');
    });

    // Set initial active toggle
    $("[data-toggle='treeview.'].is-expanded").parent().toggleClass('is-expanded');

    //Activate bootstrip tooltips
    $("[data-toggle='tooltip']").tooltip();

})();


/*
	Funciones globales javascript para el sistema
 */

function show_error_form(errors) {
    $('.show-errors').html("");
    let html = "";
    for (let i in errors.responseJSON.error) {
        html += '<div class="alert alert-danger" ' + '<strong>' + i.toUpperCase() + ': </strong>' + errors.responseJSON.error[i] + '<button class="close" type="button" data-dismiss="alert">×</button>' + '</div>'
    }
    console.log(html);
    $('.show-errors').append(html);
}

function show_notify_success(message) {
    $.notify({
        title: '',
        message: message,
        icon: 'fa fa-check'
    }, {
        type: "success",
        allow_dismiss: true,
        newest_on_top: false,
        showProgressbar: false,
        timer: 1500,
        delay: 500,
        placement: {
            from: "top",
            align: "right"
        },
        animate: {
            enter: 'animate__animated animate__fadeInDown',
            exit: 'animate__animated animate__fadeOutUp'
        },
    });
}

function show_notify_error(message) {
    $.notify({
        title: '',
        message: message,
        icon: 'fas fa-exclamation-circle'
    }, {
        type: "danger",
        allow_dismiss: true,
        newest_on_top: false,
        showProgressbar: false,
        timer: 1500,
        delay: 500,
        placement: {
            from: "top",
            align: "right"
        },
        animate: {
            enter: 'animate__animated animate__fadeInDown',
            exit: 'animate__animated animate__fadeOutUp'
        },
    });
}

function show_error_json(title, errors) {

    let html = "";
    for (let i in errors.responseJSON.error) {
        html += '<p>' + '<strong>' + i.toUpperCase() + ': </strong>' + errors.responseJSON.error[i]  + '</p>'
    }

    Swal.fire({
        title: title,
        html: html,
        icon: 'error'
    });
}

function mensaje_error(title, text){
     Swal.fire({
        title: title,
        text: text,
        icon: 'error',
    });
}

function mensaje_success(title, text){
     Swal.fire({
        title: title,
        text: text,
        icon: 'success',
    });
}

function mensaje_succes_func(title, text, func){
    Swal.fire({
        title: title,
        text: text,
        icon: 'success',
    }).then(function () {
         func();
     });
}

function alert_delete_custom(title, text, func){
    Swal.fire({
        title: title,
        text: text,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar!'
    }).then((result) => {
        if (result.isConfirmed) {
            func();
        }
    })
}