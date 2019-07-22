$(document).ready(function() {

    $(".custom-file-input").on("change", function(event) {
        $(this).next(".custom-file-label").html(event.target.files[0].name);

        $("#process-button").click(function () {
            var spinner = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
            $(this).addClass("disabled");
            $(this).append(spinner);
        });
    });
});
