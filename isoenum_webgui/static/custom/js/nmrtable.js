$(document).ready(function() {
    $(function(){
        $('#select-all-button').on('click', function() {
            $(".parent-checkbox").each(function(index){
                var checkboxSelectAll = $(this);
                var checkboxGroup = $(this).data("group");

                checkboxSelectAll.prop('checked', true);
                $(checkboxGroup).prop('checked', true);
            });
        });
    });

    $(function(){
        $('#deselect-all-button').on('click', function() {
            $(".parent-checkbox").each(function(index){
                var checkboxSelectAll = $(this);
                var checkboxGroup = $(this).data("group");

                checkboxSelectAll.prop('checked', false);
                $(checkboxGroup).prop('checked', false);
            });
        });
    });

    $(function(){
        $(".parent-checkbox").each(function(index){
            var checkboxSelectAll = $(this);
            var checkboxGroup = $(this).data("group");

            checkboxSelectAll.change(function(){  // Select all change
                 $(checkboxGroup).prop('checked', checkboxSelectAll.prop("checked"));
            });
            $(checkboxGroup).change(function(){  // Individual checkboxes change
                checkboxSelectAll.prop('checked', false);
                if ($(checkboxGroup+':checked').length === $(checkboxGroup).length ){
                    checkboxSelectAll.prop('checked', true);
                }
            });
        });
    });

    var findSelectedRows = function() {
        var selectedRows = [];

        $.each($("td input"), function() {
            if ($(this).prop("checked")) {
                selectedRows.push($(this).closest("tr").attr("id"));
            }
        });
        return selectedRows;
    };

    $(function() {
        $("#save-csv").click(function () {
            var selectedRows = findSelectedRows();
            $("#nmr-table-data").val(selectedRows);
        });
    });
});
