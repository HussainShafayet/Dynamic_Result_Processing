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
    $('#remove_user').on('click', function() {
        return confirm("Are you sure!!!");
    });
    $('#icon').click(function() {
        if ($(window).on("click")) {
            $('#side-menu').slideToggle();
            console.log(1)
        } else {
            $('#side-menu').slideToggle(500);
            $('#side-menu').css({
                'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)'
            })
        }
    });

    $('.stud_del').on('click', function() {
        return confirm("Are you sure!!!");
    });
    $('.submit').on('click', function() {
        return confirm("Are you complete Calculate GPA ???");
    });
    $('#delete_course').on('click', function() {
        return confirm("Are you sure???")
    });
    $('#submit_result').on('click', function() {
        return confirm("Please Calculate result first.")
    });

});