import os
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from tuitionapp.models import Course,TeacherAttendance,StudentAttendance,Task,Tasksubmission
from .models import CustomUser, Usermember
from django.contrib.auth.models import auth
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password

def home(request):
    return render(request, 'home.html')

def login1(request):
    return render(request, 'login.html')

def t_reg(request):
    courses = Course.objects.all()
    return render(request, 'teacher_reg.html', {'courses': courses})

def s_reg(request):
    courses = Course.objects.all()
    return render(request, 'student_reg.html', {'courses': courses})

def adminhome(request):
    pending_requests = CustomUser.objects.filter(status='0').count()
    pending_requests_count = pending_requests-1
    tt = CustomUser.objects.filter(user_type='2').count()
    ts = CustomUser.objects.filter(user_type='3').count()
    tc = Course.objects.count()
    pt = CustomUser.objects.filter(user_type='2', status=False).count()
    ps = CustomUser.objects.filter(user_type='3', status=False).count()
    tst = CustomUser.objects.filter(status=True).count()
    return render(request, 'adminhome.html', {'pending_requests_count': pending_requests_count,'tt': tt,'ts': ts,'tc':tc,'pt':pt,'ps':ps,'tst':tst})

def course(request):
    pending_requests = CustomUser.objects.filter(status='0').count()
    pending_requests_count = pending_requests-1
    return render(request, 'addcourse.html',{'pending_requests_count': pending_requests_count})

def add_course(request):
    if request.method == 'POST':
        cname = request.POST.get('cname')
        duration = request.POST.get('duration')
        file = request.FILES.get('file')
        fee = request.POST.get('fee')
        course = Course(coursename=cname, duration=duration, syllabus=file, fee=fee)
        course.save()
        messages.success(request, 'Course Added Successfully!!!')
        return redirect('course')
    return render(request, 'adminhome.html')

def view_course(request):
    pending_requests = CustomUser.objects.filter(status='0').count()
    pending_requests_count = pending_requests-1
    courses = Course.objects.all()
    return render(request, 'viewcourse.html', {'courses': courses,'pending_requests_count': pending_requests_count})

""" def edit_course(request, pk):
    pending_requests = CustomUser.objects.filter(status='0').count()
    pending_requests_count = pending_requests-1
    course = Course.objects.get(id=pk)
    return render(request, 'editcourse.html', {'course': course,'pending_requests_count': pending_requests_count})

def edit_course1(request, pk):
    if request.method == 'POST':
        course = Course.objects.get(pk=pk)
        course.coursename = request.POST.get('cname')
        course.duration = request.POST.get('duration')
        course.fee = request.POST.get('fee')

        if 'file' in request.FILES:
            new_syllabus = request.FILES['file']
            if course.syllabus:
                course.syllabus.delete()
            course.syllabus = new_syllabus
        course.save()
        return redirect('view_course') 
    return render(request, 'viewcourse.html')

def delete_course(request, pk):
    course = Course.objects.get(id=pk)
    course.delete()
    return redirect('view_course') """

def logout1(request):
    auth.logout(request)
    return redirect('home')

def login_user(request):
    if request.method == "POST":
        user_name = request.POST.get('uname')
        password1 = request.POST.get('pswd')
        user = authenticate(username=user_name, password=password1)

        if user is not None:
            login(request, user)
            if user.user_type == '1':
                return redirect('adminhome')
            elif user.user_type == '2':
                return redirect('teacherhome')
            else:
                return redirect('studenthome')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login1')
    return render(request, 'login.html')

def sregistration(request):
    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        user_name = request.POST['uname']
        age = request.POST['age']
        contact = request.POST['num']
        email = request.POST['email']
        image=request.FILES['image']
        user_type = request.POST['text']
        sel = request.POST.get('sel')
        coursename = Course.objects.get(id=sel)

        if CustomUser.objects.filter(username=user_name)or CustomUser.objects.filter(email=email).exists():
            messages.info(request, 'This username or email  already exists!!!')
            return render(request, 'student_reg.html')
        else:
            user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, username=user_name,
                                                    email=email, user_type=user_type)
            user.save()
            stud = Usermember(age=age, contact=contact, image=image, user=user, course=coursename)
            stud.save()
            subject = "Registration Confirmation"
            message = "Registration successful, Wait for admin approval"
            send_mail(subject, f"Hello {user.username} {message}", settings.EMAIL_HOST_USER, [email])
            messages.success(request, 'User registration successful. Please wait for admin approval')
            return redirect('sregistration')
    return render(request, 'student_reg.html')  
        
def tregistration(request):
    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        user_name = request.POST['uname']
        age = request.POST['age']
        contact = request.POST['num']
        email = request.POST['email']
        image = request.FILES['image']
        user_type = request.POST['text']
        sel = request.POST.get('sel')
        coursename = Course.objects.get(id=sel)

        if CustomUser.objects.filter(username=user_name).exists():
            messages.info(request, 'This username already exists!!!')
            return render(request, 'teacher_reg.html')
        else:
            user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, username=user_name,
                                                    email=email, user_type=user_type)
            user.save()
            teach = Usermember(age=age, contact=contact, image=image, user=user, course=coursename)
            teach.save()
            subject = "Registration Confirmation"
            message = "Registration successful, Wait for admin approval"
            send_mail(subject, f"Hello {user.username} {message}", settings.EMAIL_HOST_USER, [email])
            messages.success(request, 'User registration successful. Please wait for admin approval')
            return redirect('tregistration')

    return render(request, 'teacher_reg.html')  
        
def approve_disapprove(request):
    pending_requests = CustomUser.objects.filter(status='0').count()
    pending_requests_count = pending_requests-1
    user=CustomUser.objects.filter(~Q(user_type=1))
    return render(request,'approve_disapprove.html',{'user':user ,'pending_requests_count': pending_requests_count})

def approve(request, pk):
    user = CustomUser.objects.get(id=pk)
    if user.user_type == '2' or user.user_type == '3':
        user.status = '1'
        user.save()
        password = str(random.randint(100000, 999999))
        user.set_password(password)
        user.save()
        subject = 'Registration Approved'
        message = f'Your registration has been approved.\n\nUsername: {user.username}\nPassword: {password}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
        messages.success(request, 'User approved and email sent')
    else:
        user.status = '0'
        user.save()
        messages.error(request, 'Invalid user type')
    return HttpResponseRedirect(reverse('approve_disapprove'))

def disapprove(request, pk):
    user = get_object_or_404(CustomUser, id=pk)
    user_member = Usermember.objects.filter(user=user).first()
    if user_member:
        user_member.delete()
    user.delete()
    return redirect('approve_disapprove')

def show_teacher(request):
    pending_requests = CustomUser.objects.filter(status='0').count()
    pending_requests_count = pending_requests-1
    teach=Usermember.objects.all()
    u=CustomUser.objects.all()
    c=Course.objects.all()
    return render(request,'view_teacher.html',{'teach':teach,'u':u,'c':c,'pending_requests_count': pending_requests_count})

def show_student(request):
    pending_requests = CustomUser.objects.filter(status='0').count()
    pending_requests_count = pending_requests-1
    stud=Usermember.objects.all()
    u1=CustomUser.objects.all()
    c1=Course.objects.all()
    return render(request,'view_student.html',{'stud':stud,'u1':u1,'c1':c1,'pending_requests_count': pending_requests_count})

def delete_student(request,pk):
    student=get_object_or_404(Usermember, pk=pk)
    user=student.user
    user.delete()
    return redirect('show_student')
    

def delete_teacher(request, pk):
    teacher = get_object_or_404(Usermember, pk=pk)
    associated_students = Usermember.objects.filter(current_teacher=teacher.user)

    for student in associated_students:
        student.current_teacher = None
        student.save()
    
    teacher.user.delete()
    teacher.delete()
    return redirect('show_teacher')   

    
def add_tattendance(request):
    pending_requests = CustomUser.objects.filter(status='0').count()
    pending_requests_count = pending_requests-1
    teachers=CustomUser.objects.filter(user_type='2')  
    return render(request, 'teacher_attendance.html', {'teachers': teachers,'pending_requests_count': pending_requests_count})

def teach_attend(request):
    if request.method == 'POST':
        tname_id = request.POST['sel']
        t_na = CustomUser.objects.get(id=tname_id)
        date = request.POST['date']
        attendance = request.POST['status']

        if TeacherAttendance.objects.filter(teacher_name=t_na, date=date).exists():
            messages.error(request, 'Attendance for this teacher on this date already marked!')
            return redirect('add_tattendance')
        
        teach_attendance = TeacherAttendance(teacher_name=t_na, date=date, attendance=attendance)
        teach_attendance.save()
        messages.info(request, 'Attendance added')
        return redirect('add_tattendance')

    
def view_tattendance(request):
    pending_requests = CustomUser.objects.filter(status='0').count()
    pending_requests_count = pending_requests-1
    teach_names=CustomUser.objects.filter(user_type='2', status=True)
    return render(request, 'view_teacherattend.html', {'teach_names': teach_names,'pending_requests_count': pending_requests_count})

def view_teacher_attendance(request):
    if request.method == 'POST':
        opt=request.POST.get('sel')
        teacher=Usermember.objects.get(user=opt).user
        start_date=request.POST.get('s_date')
        end_date=request.POST.get('e_date')
        attendances=TeacherAttendance.objects.filter(teacher_name=teacher, date__range=[start_date, end_date])
        return render(request, 'view_teacherattend.html', {'teacher': teacher, 'attendances': attendances})
    return render(request, 'view_teacherattend.html')

def view_teacher_attendance_list(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('sel')
        start_date = request.POST.get('s_date')
        end_date = request.POST.get('e_date')
        attendances = TeacherAttendance.objects.filter(teacher_name_id=teacher_id, date__range=[start_date, end_date])
        return render(request, 'teach_attendlist.html', {'attendances': attendances})
    else:
        teach_names=CustomUser.objects.filter(user_type='2', status=True)
        return render(request, 'view_teacher_attendance.html', {'teach_names': teach_names})

def assign(request):
    pending_requests = CustomUser.objects.filter(status='0').count()
    pending_requests_count = pending_requests-1
    courses = Course.objects.all()
    students = Usermember.objects.filter(user__user_type='3')  
    teachers = Usermember.objects.filter(user__user_type='2') 
    return render(request, 'assign_teachers.html', {'courses': courses, 'students': students, 'teachers': teachers,'pending_requests_count': pending_requests_count})

def assign_teacher(request, student_id, teacher_id):
    student = CustomUser.objects.get(id=student_id)
    teacher = CustomUser.objects.get(id=teacher_id)
    user_member = Usermember.objects.get(user=student)
    user_member.current_teacher = teacher
    user_member.save()
    return redirect('assign')


def teacherhome(request):
    teacher = request.user
    usermember = Usermember.objects.filter(user=teacher).first()  
    course = usermember.course
    return render(request, 'teacherhome.html', {'teacher': teacher, 'usermember': usermember,'course':course})

def view_syllabus(request):
    if request.user.is_authenticated and request.user.status and request.user.user_type == '2':
        user_id = request.user.id
        courses = Course.objects.filter(usermember__user_id=user_id)
        return render(request, 'view_syllabus.html', {'courses': courses})
    else:
        return redirect('teacherhome')
    
def attend_teach(request):
    return render(request,'attendance_view_teach.html')
    
def show_teacher_attendance_list(request):
    if request.method == 'POST':
        start_date = request.POST.get('s_date')
        end_date = request.POST.get('e_date')
        teacher = request.user 
        attendances = TeacherAttendance.objects.filter(teacher_name=teacher, date__range=[start_date, end_date])
        return render(request, 'attendanceteacherlist.html', {'attendances': attendances})
    return render(request, 'attendance_view_teach.html')

def add_sattendance(request):
    teacher = request.user
    students = CustomUser.objects.filter(user_type='3', teacher_student_assignment__current_teacher=teacher)
    
    return render(request, 'mark_student_attend.html', {'students': students})

def stud_attend(request):
    if request.method == 'POST':
        sname_id = request.POST['sel']
        s_na = CustomUser.objects.get(id=sname_id)
        date = request.POST['date']
        attendance = request.POST['status']
        
        if StudentAttendance.objects.filter(student_name=s_na, date=date).exists():
            messages.error(request, 'Attendance for this student on this date already marked!')
            return redirect('add_sattendance')
        
        stud_attendance = StudentAttendance(student_name=s_na, date=date, attendance=attendance)
        stud_attendance.save()
        messages.info(request, 'Attendance added')
        return redirect('add_sattendance')
    
def view_sattendance(request):
    teacher = request.user
    stud_names=CustomUser.objects.filter(user_type='3', teacher_student_assignment__current_teacher=teacher)
    return render(request, 'view_studentattend.html', {'stud_names': stud_names})

def view_student_attendance(request):
    if request.method == 'POST':
        opt=request.POST.get('sel')
        student=Usermember.objects.get(user=opt).user
        start_date=request.POST.get('s_date')
        end_date=request.POST.get('e_date')
        attendances=TeacherAttendance.objects.filter(student_name=student, date__range=[start_date, end_date])
        return render(request, 'view_studentattend.html', {'student': student, 'attendances': attendances})
    return render(request, 'view_studentattend.html')

def view_student_attendance_list(request):
    if request.method == 'POST':
        student_id = request.POST.get('sel')
        start_date = request.POST.get('s_date')
        end_date = request.POST.get('e_date')
        attendances = StudentAttendance.objects.filter(student_name_id=student_id, date__range=[start_date, end_date])
        
        return render(request, 'stud_attendlist.html', {'attendances': attendances})
    else:
        stud_names = CustomUser.objects.filter(user_type='3', status=True)
        return render(request, 'view_studentattend.html', {'stud_names': stud_names})
    
def teach_view_student(request): 
    teacher = request.user
    students = Usermember.objects.filter(current_teacher=teacher)
    return render(request, 'teachviewstud.html', {'stud': students})

def task(request):
    teacher = request.user
    stud_names=CustomUser.objects.filter(user_type='3', teacher_student_assignment__current_teacher=teacher)
    return render(request,'assign_task.html', {'stud_names': stud_names})

def assign_task(request):
    if request.method == 'POST':
        taskname = request.POST.get('tname')
        sdate = request.POST.get('s_date')
        edate = request.POST.get('e_date')
        teacher_user = request.user
        teacher_member = Usermember.objects.get(user=teacher_user)
        task = Task(task_name=taskname, start_date=sdate, end_date=edate, teacher=teacher_member)
        task.save()
        messages.success(request, 'Task Send Successfully!!!')
        return redirect('task')
    return render(request, 'teacherhome.html')

def view_task(request):
    teacher = request.user
    usermember = Usermember.objects.filter(user=teacher).first()
    if usermember:
        tasks = Task.objects.filter(teacher=usermember)
        return render(request, 'view_tasks.html', {'tasks': tasks})

def studenthome(request):
    student = request.user
    usermember = Usermember.objects.filter(user=student).first()  
    course = usermember.course
    return render(request, 'studenthome.html', {'student': student, 'usermember': usermember,'course':course})

def attend_stud(request):
    return render(request,'attendance_view_stud.html')
    
def show_student_attendance_list(request):
    if request.method == 'POST':
        start_date = request.POST.get('s_date')
        end_date = request.POST.get('e_date')
        student = request.user 
        attendances = StudentAttendance.objects.filter(student_name=student, date__range=[start_date, end_date])
        return render(request, 'attendancestudentlist.html', {'attendances': attendances})
    return render(request, 'attendance_view_stud.html')

def view_syllabus_stud(request):
    if request.user.is_authenticated and request.user.status and request.user.user_type == '3':
        user_id = request.user.id
        courses = Course.objects.filter(usermember__user_id=user_id)
        return render(request, 'viewsyllabus_stud.html', {'courses': courses})
    
#ADMIN(view)
def view_studattendance(request):
    pending_requests = CustomUser.objects.filter(status='0').count()
    pending_requests_count = pending_requests-1
    stud_names=CustomUser.objects.filter(user_type='3', status=True)
    return render(request, 'view_all_stud_attend.html', {'stud_names': stud_names,'pending_requests_count': pending_requests_count})

def view_stud_attendance(request):
    if request.method == 'POST':
        opt=request.POST.get('sel')
        student=Usermember.objects.get(user=opt).user
        start_date=request.POST.get('s_date')
        end_date=request.POST.get('e_date')
        attendances=TeacherAttendance.objects.filter(student_name=student, date__range=[start_date, end_date])
        return render(request, 'view_all_stud_attend.html', {'student': student, 'attendances': attendances})
    return render(request, 'view_all_stud_attend.html')

def view_all_student_attendance_list(request):
    if request.method == 'POST':
        student_id = request.POST.get('sel')
        start_date = request.POST.get('s_date')
        end_date = request.POST.get('e_date')
        attendances = StudentAttendance.objects.filter(student_name_id=student_id, date__range=[start_date, end_date])
        student = CustomUser.objects.get(id=student_id)
        usermember = Usermember.objects.filter(user=student).first()
        course_name = usermember.course.coursename if usermember else None
        return render(request, 'allstud_attendlist.html', {'attendances': attendances, 'course_name': course_name})
    else:
        stud_names = CustomUser.objects.filter(user_type='3', status=True)
        return render(request, 'view_all_studattend.html', {'stud_names': stud_names})
#---
    
def course_view(request):
    user = request.user
    u = Usermember.objects.get(user=user)
    course = u.course  
    return render(request, 'course_details.html', {'u': u,'course': course,})

def profile(request):
    student = request.user
    s = Usermember.objects.get(user=student)
    return render(request, 'stud_profile.html', {'s': s})

def edit_pro(request):
    return render(request, 'edit_profile.html')

def edit_profile(request):
    if request.method == 'POST':
        u = request.user
        u1 = Usermember.objects.get(user=u)
        u.first_name = request.POST.get('fname')
        u.last_name = request.POST.get('lname')
        u.username = request.POST.get('uname')
        u.email = request.POST.get('email')
        u.save()
        u1.age = request.POST.get('age')
        u1.contact = request.POST.get('num')
        if len(request.FILES)!=0:
            if len(u1.image)>0:
                os.remove(u1.image.path)
            u1.image=request.FILES.get('image')
        u1.save()
        return redirect('profile') 
    else:
        u = request.user
        u1 = Usermember.objects.get(user=u)
        return render(request, 'edit_profile.html', {'u': u, 'u1': u1})

def student_task_view(request):
    student = request.user
    usermember = Usermember.objects.filter(user=student).first()
    if usermember and usermember.current_teacher:
        current_teacher = usermember.current_teacher
        tasks = Task.objects.filter(teacher__user=current_teacher)
        submitted_tasks = Tasksubmission.objects.filter(student=usermember)
        s = submitted_tasks.values_list('task_id', flat=True)
        for task in tasks:
            task.submit_user = task.id in s
        return render(request, 'view_task_student.html', {'tasks': tasks, 'usermember': usermember})

def task_submit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'submit_task.html', {'task': task})

def submit_task(request, task_id):
    if request.method == 'POST': 
        task = get_object_or_404(Task, pk=task_id)
        task_file = request.FILES.get('task_upload')
        description = request.POST.get('desc')
        student = Usermember.objects.get(user=request.user)  
        task_submission = Tasksubmission(task=task, task_upload=task_file, description=description, student=student)
        task_submission.save()
        messages.success(request, 'Task Submitted Successfully!!!')
        return redirect('task_submit', task_id=task_id)  
    return redirect('view_task_student') 

def view_uploaded_tasks(request):
    usermember = Usermember.objects.get(user=request.user)
    tasks = Tasksubmission.objects.filter(task__teacher=usermember)
    return render(request, 'view_uploaded_task.html', {'tasks': tasks})
    
def reset_password_stud(request):
    return render(request, 'reset_pswd_stud.html')
    
def reset_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if not check_password(old_password, request.user.password):
            messages.error(request, "Old password is incorrect")
            return redirect('reset_password')
        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match")
            return redirect('reset_password')
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, "Password updated successfully")
        return redirect('login1')
    return render(request, 'reset_pswd_stud.html')

def reset_password_teach(request):
    return render(request, 'reset_pswd_teach.html')

def reset_password1(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if not check_password(old_password, request.user.password):
            messages.error(request, "Old password is incorrect")
            return redirect('reset_password')
        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match")
            return redirect('reset_password')
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, "Password updated successfully")
        return redirect('login1')
    return render(request, 'reset_pswd_teach.html')




