from depthead.models import Course_Semester_List


def add_variable_to_context(request):
    semester = Course_Semester_List.objects.all()
    return {
        'semesters': semester,
    }
