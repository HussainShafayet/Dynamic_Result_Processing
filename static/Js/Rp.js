// When the user clicks anywhere outside of the modal, close it
var modal = document.getElementById('id01');
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

$(document).ready(function() {
    $('.select').on('change', function() {
        if (this.value == 'student') {

            $("#std").show();
            $('#teach').hide();
            $form.find('input[type=submit]').click();
        } else if (this.value == 'teacher') {
            $('#teach').show();
            $('#std').hide();

        } else {
            $("#std").hide();
            $("#teach").hide();
        }
    });
    $('#allow').on('click', function() {
        return confirm("Please Check again!!");
    });


});