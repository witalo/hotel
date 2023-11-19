function OpenAccount(pk) {
    $('#modal-account').empty();
    $.ajax({
        url: '/accounts/get_open_account/',
        async: true,
        dataType: 'json',
        type: 'GET',
        data: {'pk': pk},
        success: function (data) {
            $('#modal-account').html(data.grid).modal('show');
        },
        error: function (response) {
            toastr.error('Ocurrio un problema')
        }
    });
};

function CloseAccount(pk) {
    $('#modal-account').empty();
    $.ajax({
        url: '/accounts/get_close_account/',
        async: true,
        dataType: 'json',
        type: 'GET',
        data: {'pk': pk},
        success: function (data) {
            if (data.success) {
                $('#modal-account').html(data.grid).modal('show');
            } else {
                toastr.error(data.message);
            }
        },
        error: function (response) {
            toastr.error('Ocurrio un problema');
        }
    });
};

function ShowPaymentAccount(pk) {
    $('#modal-account').empty();
    $.ajax({
        url: '/accounts/modal_payments/',
        async: true,
        dataType: 'json',
        type: 'GET',
        data: {'pk': pk},
        success: function (data) {
            $('#modal-account').html(data.grid).modal('show');
        },
        error: function (response) {
            toastr.error('Ocurrio un problema')
        }
    });
};

function SearchPayments(a) {
    let init = $('#init').val()
    let end = $('#end').val()
    if (init && end) {
        $.ajax({
            url: '/accounts/get_payments/',
            async: true,
            dataType: 'json',
            type: 'GET',
            data: {'pk': a, 'init': init, 'end': end},
            success: function (data) {
                $('div#payment-grid').empty().html(data.grid);
            },
            error: function (response) {
                toastr.error('Ocurrio un problema')
            }
        });
    }
}