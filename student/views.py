from django.shortcuts import render
from depthead.models import batch_result,Student_Sessions
from accounts.models import Student
from django.shortcuts import get_object_or_404

# My views here.
def student_dashboard(request):
    return render(request, 'user_dashboard.html',{'val':'user_stud'})
    
def student_result(request):
    user2 = request.user
    stud = Student.objects.get(user=user2)
    reg_no = stud.reg_no
    session = stud.session
    """ sess = get_object_or_404(Student_Sessions, Session=session)
    ses = Student_Sessions.objects.get(Session=session)
    print(ses)
    s = ses.Session """
    results = batch_result.objects.get(Reg_No=reg_no)
    contex = {
        'results':results,
    }
    return render(request,'student.html',contex)
