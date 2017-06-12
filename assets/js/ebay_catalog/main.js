/**
 * Created by alexander on 12.06.17.
 */

function initEditProductPage() {
    $('a#new_product_form_link').click(function(event) {
        var modal = $('#myModal');
        modal.modal('show');
        return false;
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