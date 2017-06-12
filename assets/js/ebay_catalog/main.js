/**
 * Created by alexander on 12.06.17.
 */

function initEditProductPage() {
    $('a#new_product_form_link').click(function(event) {
        var link = $(this);
        $.ajax({
            'url': link.attr('href'),
            'dataType': 'html',
            'type': 'get',
            'success': function (data, status, xhr) {
                // check if we got successfull response from the server
                if (status != 'success') {
                    alert('Server Error! Try again later');
                    return false;
                }
                // update modal window with arrived content from the server
                var modal = $('#myModal'), html = $(data), form = html.find('form');
                modal.find('.modal-body').html(form);
                // init our form
                initProductEditForm(form, modal);
                // setup and show modal window finally
                modal.modal({
                    'keyboard': false,
                    'backdrop': false,
                    'show': true
                });
            },
            'error': function () {
                alert('Server Error! Try again later.');
                return false;
            }
        });

        return false;
    });
}

function initProductEditForm(form, modal) {
    // close modal window on Cancel button click
    form.find('button[name="cancel_button"]').click(function(event) {
        modal.modal('hide');
        return false;
    });
    // make form work in ajax mode
    form.ajaxForm({
        'dataType': 'html',
        'error': function () {
            alert('Server Error! Try again later.')
            return false;
        },
        'success': function(data, status, xhr) {
            var html = $(data), newform = html.find('form');
            // copy alert to modal window
            modal.find('.modal-body').html(html.find('.alert'));
            // copy form to modal if we found it in server response
            if (newform.length > 0) {
                modal.find('.modal-body').append(newform);
                // initialize form fields and buttons
                initProductEditForm(newform, modal);
            } else {
                /* if no form, it means success and we need to reload page
                * to get update product list;
                * reload after 2 seconds, so that user can read
                * success message */
                setTimeout(function() {location.reload(true);}, 500);
            }
        }
    });
}

$(document).ready(function () {
    // DataTables init
    $('#ebay_data').DataTable({
        searching: false,
        "columns": [
            {"orderable": false},
            {"orderable": false},
            null,
            {"orderable": false},
            {"orderable": false},
            {"orderable": false},
            null,
            {"orderable": false},
            {"orderable": false},
            null
        ]
    });

    // Product Form modal init
    initEditProductPage();
});