$(document).on('click', 'div#inventory-list div.subsidiary-row div.subsidiary-button button.btn-stock', function () {
    let button = $(this)
    let div_button = button.parent('div.subsidiary-button')
    let subsidiary = button.attr('s')
    let product = $('#product-pk').val()
    let row = button.parent('div.subsidiary-button').parent('div.subsidiary-row')
    let input = row.find('div.subsidiary-stock div.form-group div.input-group input.input-stock')
    let quantity = input.val()
    console.log(quantity)
    if (parseFloat(quantity) > 0) {
        quantity = parseFloat(quantity).toFixed(2)
    } else {
        quantity = parseFloat('0.00').toFixed(2)
    }
    if (parseFloat(quantity) > 0) {
        let r = confirm("¿Esta seguro de crear el inventario inicial");
        if (r === true) {
            $.ajax({
                url: '/products/create_inventory/',
                dataType: 'json',
                type: 'POST',
                data: {
                       'subsidiary': subsidiary,
                       'product': product,
                       'quantity': quantity
                },
                success: function (r) {
                    if (r.success) {
                        toastr.success(r.message)
                        input.attr('disabled', 'true')
                        div_button.empty().append('<i class="fa fa-check-circle text-success fa-2x"></i>')
                    } else {
                        toastr.warning(r.message)
                    }
                },
                fail: function (r) {
                    console.log(r);
                }
            });
        }
    }else{
        toastr.info('Ingrese una cantidad valida')
        return false
    }
});