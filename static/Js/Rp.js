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
    var x = 0;
    $('.dropbtn').on('click', function() {
        $('.dropdown-content').slide("slow ");
    });
});