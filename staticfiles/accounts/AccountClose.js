$('#form-close').submit(function (event) {
    event.preventDefault();
    if ($('#id-account-close').val() === '0' || $('#id-account-close').val() === '') {
        toastr.warning('Especifique la caja que desea cerrar')
        return false;
    }
    if ($('#date-close').val() === '') {
        toastr.warning('Seleccione la fecha de cierre')
        return false;
    }
    let data = new FormData($('#form-close').get(0));
    $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function (response) {
            if (response.success) {
                toastr.success(response.message);
                setTimeout(() => {
                    location.reload();
                }, 500);
            } else {
                toastr.success(response.message);
            }
        },
        error: function (response) {
            toastr.error('¡Ocurrio un problema al cerrar la caja!');
        }
    });
});