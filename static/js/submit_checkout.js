// Get CSRF Token
function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$('#submit-btn').on('click', function(e) {
    e.preventDefault();
    const payload = {
        'first_name': $('#id_first_name').val(),
        'last_name': $('#id_last_name').val(),
        'address': $('#id_apartment_no').val() + ', ' + $('#id_street').val() + ', ' + $('#id_state').val(),
        'postal_code': $('#id_post_zip').val(),
        'city': $('#id_city_town').val(),
        'email': $('#id_email').val(),
        'phone': $('#id_phone_number').val(),
        'order_notes': $('#id_notes').val()
    }

    $.ajax({
        headers: {'X-CSRFToken': getToken('csrftoken')},
        url: '/orders/create/',
        type: 'POST',
        data: JSON.stringify(payload),
        mode: 'same_origin',
        dataType: 'json',
        success: function(response) {
            console.log(response.data.amount * 100);
            function payWithPaystack() {
              var handler = PaystackPop.setup({
                key: response.data.key,
                email: response.data.email,
                amount: response.data.amount * 100,
                currency: 'NGN',
                firstname: response.data.first_name,
                lastname: response.data.last_name,
                reference: response.data['order_ref'],
                callback: function(response) {
                  var reference = response.reference;
                  $.ajax({
                    url: '/payment/verify?reference='+ reference,
                    method: 'get',
                    success: function (response) {
                      window.location.replace('/payment/done/');
                    },
                    error: function(jqXHR, textStatus) {
                        let error_message = jqXHR.responseJSON['message'] || "Invalid Response from server";
                        let error_panel_selector = $('.error-panel');
                        error_panel_selector.text(error_message);
                        error_panel_selector.show();
                    }
                  });
                },
                onClose: function() {
                  alert('Transaction was not completed, window closed.');
                },
              });
              handler.openIframe();
            }
            payWithPaystack()
        },
        error: function(jqXHR, textStatus) {
            let error_message = jqXHR.responseJSON['message'] || "Invalid Response from server";
            let error_panel_selector = $('.error-panel');
            error_panel_selector.text(error_message);
            error_panel_selector.show();
        }
    });
});
