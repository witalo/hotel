$('#form-aperture').submit(function (event) {
    event.preventDefault();
    let data = new FormData($('#form-aperture').get(0));
    $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        headers: {"X-CSRFToken": '{{ csrf_token }}'},
        success: function (response) {
            if (response.success) {
                toastr.success(response.message);
                setTimeout(() => {
                    location.reload();
                }, 500);
            }
        },
        error: function (response) {
            toastr.error('¡Problemas al aperturar la caja!');
        }
    });
});


$("#id-amount-aperture").keyup(function (e) {
    let val = $(this).val();
    if (isNaN(val)) {
        $(this).val('');
    }
});