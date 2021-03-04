from django.shortcuts import render
from depthead.models import Result_Table, Sessions, Result_Semester_List
from accounts.models import Student
from django.shortcuts import get_object_or_404

# My views here.


def student_dashboard(request):
    return render(request, 'user_dashboard.html', {'val': 'user_stud'})


def student_result(request,semester):
    user2 = request.user
    stud = Student.objects.get(user=user2)
    reg_no = stud.reg_no
    session = stud.session
    batch = stud.batch
    get_batch = Sessions.objects.get(Batch=batch)
    get_semester = Result_Semester_List.objects.get(
        Semester=semester, session=get_batch)
    reg2 = str(batch)+' '+str(get_semester)
    get_result = Result_Table.objects.filter(
        Reg=reg2, result_semester=get_semester)

    course_list1 = []
    course_list_of_list1 = []
    course_list_of_list2 = []
    x = 0
    for i in get_result:
        field_list = i._meta.get_fields()

        for j in field_list[3:]:
            val = getattr(i, j.name)
            if val == None:
                break
            elif val == 'Name':
                x = 1
                course_list1.append(val)
            else:
                course_list1.append(val)
        if x == 1:
            course_list_of_list1.append(course_list1)
        else:
            course_list_of_list2.append(course_list1)
        course_list1 = []
        x = 2

    results = Result_Table.objects.filter(
        Reg=reg_no, batch=get_batch, result_semester=get_semester)
    list1 = []
    list_of_list1 = []
    list_of_list2 = []
    x = 0
    for i in results:

        field_list = i._meta.get_fields()
        for j in field_list[3:]:
            val = getattr(i, j.name)
            if val == None:
                break
            elif val == 'Name':
                x = 1
                list1.append(val)
            else:
                list1.append(val)
        if x == 1:
            list_of_list1.append(list1)
        else:
            list_of_list2.append(list1)
        list1 = []
        x = 2
    """ import operator
    sorted_list = sorted(list_of_list2, key=operator.itemgetter(0))
    for i in sorted_list:
        list_of_list1.append(i) """

    contex = {
        'results': list_of_list2,
        'result2': course_list_of_list1
    }
    return render(request, 'student.html', contex)
