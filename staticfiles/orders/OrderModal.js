$(function () {
    //Enable check and uncheck all functionality
    $('.checkbox-toggle').click(function () {
        var clicks = $(this).data('clicks')
        if (clicks) {
            //Uncheck all checkboxes
            $('.mailbox-messages input[type=\'checkbox\']').prop('checked', false)
            $('.checkbox-toggle .far.fa-check-square').removeClass('fa-check-square').addClass('fa-square')
        } else {
            //Check all checkboxes
            $('.mailbox-messages input[type=\'checkbox\']').prop('checked', true)
            $('.checkbox-toggle .far.fa-square').removeClass('fa-square').addClass('fa-check-square')
        }
        $(this).data('clicks', !clicks)
    })
})
$(document).ready(function () {
    new Autocomplete('#autocomplete-product', {
        search: input => {
            const url = `/products/search_product/?search=${encodeURI(input.toUpperCase())}`

            return new Promise(resolve => {
                if (input.length < 3) {
                    $('#search-code').val('')
                    return resolve([])
                }
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        resolve(data.product)
                    })
            })
        },
        renderResult: (result, props) => {
            let group = ''
            if (result.index % 3 === 0) {
                group = '<li class="group">Digite</li>'
            }
            return `
                ${group}
                <li ${props} class="font-weight-bold small">
                 <div class="text-white h5">
                    ${'<i class="spinner-grow"></i>'} ${result.name}
                 </div>
                 <div class="text-white-50 h6">
                    <b class="text-white">CODIGO: ${result.code}</b> <br>
                    MARCA : ${result.brand} <br>
                    PRECIO : ${result.price} <br>
                    STOCK : ${result.stock.quantity}
                  </div>
                </li>
                `
        },
        getResultValue: result => result.name,
        onSubmit: result => {
            if (result) {
                AddRowDetail(0, 0, result.pk, result.code, result.name, 1, result.price, result.stock.id, result.stock.quantity)
            }
        }
    })
})

async function AddRowDetail(i, pk, product, code, name, q, p, s, k) {
    let quantity = parseFloat(q).toFixed(0)
    let stock = parseFloat(k).toFixed(0)
    if (stock < quantity) {
        toastr.warning('Stock insuficiente')
        return false
    }
    let price = parseFloat(p).toFixed(2)
    let amount = parseFloat(q * p).toFixed(2)
    $('tbody#order_detail').append(
        '<tr class="p-0"  pk="' + pk + '" i="' + i + '" store="' + s + '" product="' + product + '">' +
        '<td class="align-middle item-number p-1 text-center">' +
        '<div class="icheck-primary">' +
        '<input class="input-number" type="checkbox" value="" id="' + i + '">' +
        '<label for="' + i + '">' + '</label>' +
        '</div>' +
        '</td>' +
        '<td class="mailbox-star align-middle item-quantity">' +
        '<div class="input-group input-group-sm">' +
        '<div class="input-group-prepend">' +
        '<div class="btn btn-primary btn-prev">' +
        '<i class="fa fa-minus-circle"></i>' +
        '</div>' +
        '</div>' +
        '<input type="number" min="0" step="1" value="' + quantity + '" class="form-control text-center input-quantity" placeholder="0">' +
        '<div class="input-group-append">' +
        '<div class="btn btn-primary btn-next">' +
        '<i class="fa fa-plus-circle"></i>' +
        '</div>' +
        '</div>' +
        '</div>' +
        '</td>' +
        '<td class="mailbox-subject align-middle item-name">' +
        '<b>' + 'Codigo:' + code + '</b>' + ' ' + 'Producto:' + name + '</td>' +
        '<td class="mailbox-attachment align-middle item-price">' + '<input type="number" step="0.01" min="0.00" placeholder="0.00" class="form-control form-control-sm input-price text-right" value="' + price + '" style="width: 85px;"/>' + '</td>' +
        '<td class="align-middle mailbox-date item-amount p-1 text-right">' + amount + '</td>' +
        '<td class="align-middle p-1 text-center item-delete">' +
        '    <button type="button" class="btn btn-danger rounded">' + '<i class="fa fa-trash-alt">' + '</i>' + '</button>' +
        '</td>' +
        '</tr>'
    );
    CountRow()
    TotalDetail()
}

function CountRow() {
    let index = 1;
    $('tbody#order_detail tr').each(function () {
        let div = $(this).find('td.item-number div.icheck-primary')
        div.find('input.input-number').attr('id', index)
        div.find('label').attr('for', index)
        $(this).attr('i', index);
        let pk = $(this).attr('pk');
        let product = $(this).attr('product');
        $(this).find('td.item-delete button').attr('onclick', 'DeleteRowDetail(' + index + ', ' + pk + ', ' + product + ')')
        index++;
    });
};

function TotalDetail() {
    let total = 0;
    let total_room = $('#total_room').val()
    if (total_room === '' || total_room === '0' || total_room === undefined || isNaN(total_room)) {
        total_room = parseFloat('0.00').toFixed(2)
    } else {
        total_room = parseFloat(total_room).toFixed(2)
    }
    $('tbody#order_detail tr td.item-amount').each(function () {
        if ($(this).text()) {
            total = total + parseFloat($(this).text());
        } else {
            total = total + parseFloat("0.00");
        }
    });
    let t = parseFloat(total) + parseFloat(total_room)
    $('#total').val(t.toFixed(2))
    $('#amount').val(t.toFixed(2));
};

function DeleteRowDetail(i, pk, product) {
    let rows = $('tbody#order_detail').find("tr[i=" + i + "][pk=" + pk + "][product=" + product + "]")
    if (parseInt(pk) > 0) {
        let order = $('#id-order').val()
        if (order != '' && parseInt(pk) > 0) {
            let r = confirm("¿Esta seguro de eliminar el detalle?")
            if (r == true) {
                $.ajax({
                    url: '/sales/delete_order_detail/',
                    async: true,
                    dataType: 'json',
                    type: 'GET',
                    data: {'pk': pk, 'o': 'I'},
                    success: function (response) {
                        if (response.success) {
                            rows.remove();
                            CountRow();
                            TotalDetail();
                            toastr.success(response.message)
                        } else {
                            toastr.error(response.message)
                        }
                    },
                });
            }
        } else {
            toastr.error('Necesita buscar una orden')
        }
    } else {
        rows.remove();
        CountRow();
        TotalDetail();
    }
}

function DeleteRowCheck() {
    $('tbody#order_detail tr').each(function () {
        if ($(this).find('td.item-number div.icheck-primary input.input-number').is(':checked')) {
            $(this).remove()
        }
    });
    CountRow();
    TotalDetail();
}

$(document).on('keyup change', 'tbody#order_detail tr td.item-quantity div.input-group input.input-quantity', function () {
    let input = $(this)
    let row = input.parent('div.input-group').parent('td.item-quantity').parent('tr')
    let td_amount = row.find('td.item-amount')
    let input_price = row.find('td.item-price input.input-price')
    let quantity = input.val()
    let price = input_price.val()
    if (parseFloat(quantity) > 0) {
        quantity = parseFloat(quantity).toFixed(2)
    } else {
        quantity = parseFloat('0.00').toFixed(2)
    }
    if (parseFloat(price) > 0) {
        price = parseFloat(price).toFixed(2)
    } else {
        price = parseFloat('0.00').toFixed(2)
    }
    let amount = parseFloat(quantity) * parseFloat(price)
    td_amount.text(amount.toFixed(2))
    TotalDetail()
})
$(document).on('keyup change', 'tbody#order_detail tr td.item-price input.input-price', function () {
    let input = $(this)
    let row = input.parent('td.item-price').parent('tr')
    let td_amount = row.find('td.item-amount')
    let input_quantity = row.find('td.item-quantity div.input-group input.input-quantity')
    let quantity = input_quantity.val()
    let price = input.val()
    if (parseFloat(quantity) > 0) {
        quantity = parseFloat(quantity).toFixed(2)
    } else {
        quantity = parseFloat('0.00').toFixed(2)
    }
    if (parseFloat(price) > 0) {
        price = parseFloat(price).toFixed(2)
    } else {
        price = parseFloat('0.00').toFixed(2)
    }
    let amount = parseFloat(quantity) * parseFloat(price)
    td_amount.text(amount.toFixed(2))
    TotalDetail()
})
$(document).on('click', 'tbody#order_detail tr td.item-quantity div.input-group div.input-group-prepend div.btn-prev', function () {
    let btn = $(this)
    let input_group = btn.parent('div.input-group-prepend').parent('div.input-group')
    let input = input_group.find('input.input-quantity')
    let quantity = input.val()
    if (parseInt(quantity) > 0) {
        quantity = parseInt(quantity) - 1
    } else {
        quantity = parseInt('0')
    }
    input.val(parseInt(quantity))
    input.trigger('change')
})
$(document).on('click', 'tbody#order_detail tr td.item-quantity div.input-group div.input-group-append div.btn-next', function () {
    let btn = $(this)
    let input_group = btn.parent('div.input-group-append').parent('div.input-group')
    let input = input_group.find('input.input-quantity')
    let quantity = input.val()
    console.log(quantity)
    if (parseInt(quantity) > 0) {
        quantity = parseInt(quantity)
    } else {
        quantity = parseInt('0')
    }
    quantity = quantity + 1
    input.val(parseInt(quantity))
    input.trigger('change')
})
function CreateOrder(){
    let order = $('#order').val()
    let client = $('#client').val()
    let init = $('#init').val()
    let end = $('#end').val()
    let total_room = $('#total_room').val()
    var state = $("input[type='radio'][name='state']:checked").val();
    let Order = {
        "Detail": [],
        "order": order,
        "client": client,
        "init": init,
        "end": end,
        "price": total_room,
        "state": state,
    };
    let status = true
    $("tbody#order_detail tr").each(function () {
        let row = $(this)
        let pk = row.attr('pk')
        let i = row.attr('i')
        let store = row.attr('store')
        if (store === '0' || store === '' || store === undefined) {
            toastr.info('Almacen desconocido en la fila ' + i.toString())
            status = false
            return status
        }
        let product = row.attr('product')
        if (product === '0' || product === '' || product === undefined) {
            toastr.info('Producto desconocido en la fila ' + i.toString())
            status = false
            return status
        }
        let quantity = row.find('td.item-quantity div.input-group input.input-quantity').val()
        if (parseFloat(quantity) === 0 || quantity === '' || quantity === undefined) {
            toastr.info('Ingrese una cantidad en la fila ' + i.toString())
            status = false
            return status
        }
        let price = row.find('td.item-price input.input-price').val()
        if (parseFloat(price) === 0 || price === '' || price === undefined) {
            toastr.info('Ingrese un precio en la fila ' + i.toString())
            status = false
            return status
        }
        let Detail = {
            "detail": pk,
            "product": product,
            "quantity": parseFloat(quantity).toFixed(2),
            "price": parseFloat(price).toFixed(2),
            "store": parseInt(store)
        };
        Order.Detail.push(Detail);
    })
    if (!status) {
        return false
    } else {
        SendOrder(Order)
    }
}
function SendOrder(object) {
    console.log(object)
    let r = confirm('¿ESTA SEGURO DE PROCESAR LA ORDEN?');
    if (r === true) {
        $.ajax({
            url: '/orders/create_order/',
            dataType: 'json',
            type: 'POST',
            data: {'order': JSON.stringify(object)},
            success: function (response) {
                if (response.success) {
                    toastr.success(response.message)
                    CleanSales()
                } else {
                    toastr.error(response.message)
                }
            },
            error: function (jqXhr, textStatus, xhr) {
                if (jqXhr.status === 500) {
                    toastr.error(jqXhr.responseJSON.error);
                }
            }
        });
    }
}