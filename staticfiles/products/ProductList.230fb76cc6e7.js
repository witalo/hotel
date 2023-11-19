function ShowModalInventory(n) {
    $.ajax({
        url: '/products/modal_inventory/',
        dataType: 'json',
        type: 'GET',
        data: {'pk': n},
        success: function (r) {
            if (r.success) {
                $('#modal-inventory').empty().html(r.form).modal('show');
            } else {
                toastr.warning(r.message)
            }
        },
        fail: function (r) {
            toastr.error(r);
        }
    });
};