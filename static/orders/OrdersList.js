function SearchOrders() {
    let init = $('#init').val()
    let end = $('#end').val()
    let type = $('#type').val()
    if (init && end) {
        $.ajax({
            url: '/orders/get_orders/',
            async: true,
            dataType: 'json',
            type: 'GET',
            data: {'type': type, 'init': init, 'end': end},
            success: function (r) {
                $('div#orders-grid').empty().html(r.grid);
            },
            error: function (r) {
                toastr.error('Ocurrio un problema')
            }
        });
    }
}

function Ticket(o) {
    if (parseInt(o) > 0) {
        $.ajax({
            url: "/orders/ticket/" + o + "/",
            method: "GET",
            xhrFields: {
                responseType: 'blob'
            },
            success: function (data) {
                const blob = new Blob([data], {type: 'application/pdf'});
                const link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                const pdfUrl = link.href;

                // Cargar el PDF en el iframe del modal y mostrar el modal
                $("#pdfFrame").attr("src", pdfUrl);
                $("#pdfModal").modal("show");
            },
            error: function (error) {
                console.error("Error al obtener el PDF:", error);
            }
        });
    }
}

function TicketRefund(o) {
    if (parseInt(o) > 0) {
        $.ajax({
            url: "/orders/ticket_refund/" + o + "/",
            method: "GET",
            xhrFields: {
                responseType: 'blob'
            },
            success: function (data) {
                const blob = new Blob([data], {type: 'application/pdf'});
                const link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                const pdfUrl = link.href;

                // Cargar el PDF en el iframe del modal y mostrar el modal
                $("#pdfFrame").attr("src", pdfUrl);
                $("#pdfModal").modal("show");
            },
            error: function (error) {
                console.error("Error al obtener el PDF:", error);
            }
        });
    }
}