$(document).ready(function() {
    $(function(){
        $("tbody").on("click", ".popup", function(event) {
            event.preventDefault();
            window.open($(this).attr("href"), "popupWindow", "width=800,height=600,scrollbars=yes");
        });
    });
});
