// function ReloadRoom(p) {
//     $('#room-list').empty()
//     if (parseInt(p)) {
//         $.ajax({
//             url: '/rooms/get_rooms/',
//             dataType: 'json',
//             type: 'GET',
//             data: {'pk': p},
//             success: function (r) {
//                 if (r.success) {
//                     AddRooms(r['room'])
//                 } else {
//                     toastr.warning(r.message)
//                 }
//             },
//             error: function (r) {
//                 toastr.error(r);
//             }
//         });
//     }
// }

function ReloadRoom(p) {
    $('#room-list').empty()
    if (parseInt(p)) {
        $.ajax({
            url: '/rooms/get_rooms_grid/',
            dataType: 'json',
            type: 'GET',
            data: {'pk': p},
            success: function (r) {
                if (r.success) {
                    $('#order-grid').empty().html(r.grid)
                } else {
                    toastr.warning(r.message)
                }
            },
            error: function (r) {
                toastr.error(r);
            }
        });
    }
}

async function AddRooms(room) {
    for (let i = 0; i < room.length; i++) {
        await AddRow(room[i].id, room[i].number, room[i].name, room[i].t, room[i].type, room[i].state)
    }
}

function AddRow(id, number, name, t, type, state) {
    $('#room-list').append(
        '<div class="filtr-item col-sm-2 p-1" data-category="' + t + '">' +
        '<a href="https://via.placeholder.com/1200/' + state + '.png?text=' + number + '" data-toggle="lightbox" class="w-100" data-title="sample 1 - white">' +
        '<div class="ribbon-wrapper ribbon-lg m-1">' +
        '<div class="ribbon bg-gradient-purple">' + type +
        '</div>' +
        '</div>' +
        '<img src="https://via.placeholder.com/300/' + state + '?text=' + number + '" class="img-fluid w-100" alt="white sample"/>' +
        '</a>' +
        '</div>'
    )
}

function ShowModalOrder(pk) {
    $.ajax({
        url: '/orders/modal_orders/',
        dataType: 'json',
        type: 'GET',
        data: {'pk': pk},
        success: function (response) {
            if (response.success) {
                $('#modal-order').empty().html(response.form).modal('show');
            } else {
                toastr.warning(response.message)
            }
        },
        fail: function (response) {
            toastr.error('Error en la petición');
        }
    });
};
