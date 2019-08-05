$(document).ready(function() {
    $(function(){
        $(".popup").click(function(event) {
            event.preventDefault();
            window.open($(this).attr("href"), "popupWindow", "width=800,height=600,scrollbars=yes");
        });
    });
});