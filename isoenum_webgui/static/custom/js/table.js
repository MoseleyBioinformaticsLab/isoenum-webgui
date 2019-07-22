$(document).ready(function() {

    var $inchiTable = $("table#inchi-table");
    var $numberOfColumns = $("table#inchi-table > thead > tr > th").length;

    $(function() {
        $("#generate-nmr-button").click(function () {
            var NMRExperimentType = $("#select-nmr-experiment-button").val();
            var tableRows = tableToJSON('#inchi-table');
            $("#nmr-table-data").val(JSON.stringify(tableRows));

        });
    });

    $(function() {
       $inchiTable.on('click', 'tr', function() {
           if ($(this).is(('#inchi-table-header'))) {}
           else {
               $(this).addClass('highlight').siblings().removeClass('highlight');
           }
       });
    });


    function applyTooltip(tdElement, errorMessage) {
        tdElement.tooltip("dispose");
        tdElement.addClass("bg-danger");
        tdElement.attr("title", "Incorrect isotope specification: " + errorMessage);
        tdElement.attr("data-toggle", "tooltip");
        tdElement.attr("data-placement", "top");
        tdElement.tooltip("enable");
        tdElement.tooltip("show");
    }

    function removeTooltip(tdElement) {
        tdElement.removeClass("bg-danger");
        tdElement.attr("title", "");
        tdElement.tooltip("dispose");
    }

    $(function() {
        $('tbody').on('click', '.update-row-button', function() {
            var record_id = $(this).closest('tr').attr('id');
            var record_data = rowToJSON('table', record_id);
            var tdISO = $("tr#" + record_id + " > td.ISO");
            var tdCHG = $("tr#" + record_id + " > td.CHG");
            var tdBaseIdentifier = $("tr#" + record_id + " > td.Base.Identifier");

            var request = $.ajax({
                url: '/update_record',
                type: 'POST',
                data: record_data
            });

            request.fail(function() {

                var errorType = request.responseJSON.error.type;
                var errorMessage = request.responseJSON.error.message;

                if (errorType === "IsotopeSpecError") {
                    applyTooltip(tdISO, errorMessage);
                }

                if (errorType === "ChargeSpecError") {
                    applyTooltip(tdCHG, errorMessage);
                }

            });

            request.done(function(data) {

                removeTooltip(tdISO);
                removeTooltip(tdCHG);

                $('tr#' + record_id + ' > td.Base.SVG').html(data["Base SVG"]);
                $('tr#' + record_id + ' > td.ISO').html(data["ISO"]);
                $('tr#' + record_id + ' > td.CHG').html(data["CHG"]);
                $('tr#' + record_id + ' > td.Repr.Identifier').html(data["Repr Identifier"]);
                $('tr#' + record_id + ' > td.Repr.SVG').html(data["Repr SVG"]);
            });
        });
    });

    $(function() {
        $('tbody').on('click', '.remove-row-button', function() {
            var record_id = $(this).closest('tr').attr('id');

            var request = $.ajax({
                url: '/remove_record',
                type: 'POST',
                data: {'record_id': record_id}
            });

            request.done(function(data) {
                if (data['success']) {
                    $("tr#" + record_id).remove();
                }
                else {
                    alert("Cannot remove record: " + record_id);
                }
            });
        });
    });

    $(function() {
        $(".add-row-button").click(function() {
            var record_id = $(this).attr('record_id');
            var current_tr = $('tr#' + record_id);

            var request = $.ajax({
                url: '/add_record',
                type: 'POST'
            });

            request.done(function(data) {
                alert(data['record_id'])
            });
            console.log(current_tr);
        });
    });

    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });

    $(function() {
        $("#add-button").on('click', function () {

            var request = $.ajax({
                url: '/add_record',
                type: 'POST'
            });

            request.done(function(data) {
                var record_id = data['record_id'];
                var tr = $('<tr id=' + record_id + '>');
                    tr.append($('<td class="pt-3-half align-middle Name" contenteditable="true" spellcheck="false"></td>'));
                    tr.append($('<td class="pt-3-half align-middle Base Identifier" contenteditable="true" spellcheck="false"></td>'));
                    tr.append($('<td class="pt-3-half align-middle Base SVG" contenteditable="false"></td>'));
                    tr.append($('<td class="pt-3-half align-middle ISO" contenteditable="true" spellcheck="false"></td>'));
                    tr.append($('<td class="pt-3-half align-middle CHG" contenteditable="true" spellcheck="false"></td>'));
                    tr.append($('<td class="pt-3-half align-middle Repr Identifier" contenteditable="false"></td>'));
                    tr.append($('<td class="pt-3-half align-middle Repr SVG" contenteditable="false"></td>'));
                    tr.append($('<td class="pt-3-half align-middle" contenteditable="false">' +
                        '<div class="btn-group-vertical">' +
                        '<button class="btn btn-primary update-row-button">Update</button>' +
                        '<button class="btn btn-light" disabled></button>' +
                        '<button class="btn btn-danger remove-row-button">Remove</button>' +
                        '</div>' +
                        '</td>'));
                $inchiTable.append(tr);
            });
        });
    });

    $("#generate-nmr-button").click(function () {
        var spinner = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
        $(this).addClass("disabled");
        $(this).append(spinner);
    });
});
