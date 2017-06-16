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

function initCsvImportPage() {
    $('a#upload_csv').click(function(event) {
        var link = $(this);
        $.ajax({
            'url': link.attr('href'),
            'dataType': 'html',
            'type': 'get',
            'success': function (data, status, xhr) {
                if (status != 'success') {
                    alert('Server Error! Try again later');
                    return false;
                }
                var modal = $('#myModal'), html = $(data), form = html.find('form');
                modal.find('.modal-body').html(form);
                initCsvImportForm(form, modal);
                modal.modal({
                    'keyboard': false,
                    'backdrop': false,
                    'show': true
                });
            },
            'error': function() {
                alert('Server Error! Try again later');
                return false;
            }
        });
        return false;
    });
}

function initCsvImportForm(form, modal) {
    form.find('button[name="cancel_button"]').click(function(event) {
        modal.modal('hide');
        return false;
    });
    form.find('button[name="upload_button"]').click(function(event) {
        var btn = $(this).button('loading');
        form.ajaxForm({
            'dataType': 'html',
            'error': function () {
                alert('Server Error! Try again later.');
                return false;
            },
            'success': function(data, status, xhr) {
                var html = $(data), newform = html.find('form');
                modal.find('.modal-body').html(html.find('.alert'));
                if (newform.length > 0) {
                    modal.find('.modal-body').append(newform);
                    initCsvImportForm(newform, modal);
                } else {
                    setTimeout(function() {location.reload(true);}, 500);
                }
            }
        });
    });
}

function initProductEditForm(form, modal) {
    // close modal window on Cancel button click
    form.find('button[name="cancel_button"]').click(function(event) {
        modal.modal('hide');
        return false;
    });
    // make form work in ajax mode
    form.find('button[name="add_button"]').click(function (event) {
        var btn = $(this).button('loading');
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
    });
}

function initProductsListPage() {
    $('#ebay_data').DataTable({
        'searching': false,
        'ajax': {
            'url': '/ebay-catalog/get_products/',
            'type': 'GET',
            'dataSrc': ''
        },
        'columns': [
            {'data': 'fields.product_id', 'orderable': false},
            {'data': 'fields.image', 'orderable': false},
            {'data': 'fields.rating', 'orderable': true},
            {'data': 'fields.price', 'orderable': false},
            {'data': 'fields.name', 'orderable': false},
            {'data': 'fields.in_stock', 'orderable': false},
            {'data': 'fields.qty', 'orderable': true},
            {'data': 'fields.weight', 'orderable': false},
            {'data': 'fields.length', 'orderable': false},
            {'data': 'fields.width', 'orderable': false},
            {'data': 'fields.height', 'orderable': false},
            {'data': 'fields.date_updated', 'orderable': true},
        ]
    });
}

$(document).ready(function () {
    // DataTables init
    initProductsListPage();
    // Product Form modal init
    initEditProductPage();
    // Import csv import page
    initCsvImportPage();
});