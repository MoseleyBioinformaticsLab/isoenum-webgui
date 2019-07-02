$(document).ready(function() {

    $(".custom-file-input").on("change", function(event) {
        $(this).next(".custom-file-label").html(event.target.files[0].name);
    });

});
