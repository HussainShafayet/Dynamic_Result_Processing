// When the user clicks anywhere outside of the modal, close it
var modal = document.getElementById('id01');
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

$(document).ready(function() {

    $('#allow').on('click', function() {
        return confirm("Please Check again!!");
    });

    $('#icon').click(function() {
        $('#side-menu').slideToggle(1000);
        $('#side-menu').css({
            'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)'
        })
    });

});