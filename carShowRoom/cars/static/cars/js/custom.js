/* static/cars/js/main.js */

$(function () {
    // 1. Aktifkan Tooltip Bootstrap
    $('[data-toggle="tooltip"]').tooltip();
    
    // 2. Tambahkan class form-control otomatis ke input django (agar rapi)
    $('input, select, textarea').addClass('form-control');

    // 3. Khusus textarea notes agar tidak terlalu tinggi
    $('textarea').attr('rows', 3);
});

// Script delete jadi satu dalam html