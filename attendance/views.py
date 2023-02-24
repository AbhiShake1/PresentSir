from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .filters import AttendanceFilter
from .forms import *
from .models import Student, Attendance
from .recognizer import recognizer


@login_required(login_url='login')
def home(request):
    if request.method != 'POST':
        studentForm = CreateStudentForm()
        context = {'studentForm': studentForm}
        return render(request, 'attendance_sys/home.html', context)

    studentForm = CreateStudentForm(data=request.POST, files=request.FILES)

    try:
        reg_id = request.POST['registration_id']
        Student.objects.get(registration_id=reg_id)
        stat = True
    except:
        stat = False

    if studentForm.is_valid() and not stat:
        studentForm.save()

        first_name = studentForm.cleaned_data.get('firstname')
        last_name = studentForm.cleaned_data.get('lastname')

        name = f'{first_name} {last_name}'

        messages.success(request, f'Student {name} was successfully added.')
        return redirect('home')
    else:
        reg_id = request.POST['registration_id']
        messages.error(
            request,
            f'Student with Registration Id {reg_id} already exists.'
        )
        return redirect('home')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'attendance_sys/login.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def update_student_redirect(request):
    context = {}
    if request.method == 'POST':
        try:
            reg_id = request.POST['reg_id']
            branch = request.POST['branch']
            student = Student.objects.get(
                registration_id=reg_id,
                branch=branch,
            )
            update_studentForm = CreateStudentForm(instance=student)
            context = {
                'form': update_studentForm,
                'prev_reg_id': reg_id,
                'student': student
            }
        except:
            messages.error(request, 'Student Not Found')
            return redirect('home')
    return render(
        request,
        'attendance_sys/student_update.html',
        context,
    )


@login_required(login_url='login')
def update_student(request):
    if request.method == 'POST':
        try:
            student = Student.objects.get(
                registration_id=request.POST['prev_reg_id'],
            )
            update_student_form = CreateStudentForm(
                data=request.POST,
                files=request.FILES,
                instance=student,
            )
            if update_student_form.is_valid():
                update_student_form.save()
                messages.success(request, 'Updated')
                return redirect('home')
        except:
            messages.error(request, 'Update  failed')
            return redirect('home')

    context = {}
    return render(
        request,
        'attendance_sys/student_update.html',
        context
    )


@login_required(login_url='login')
def take_attendance(request):
    if request.method != 'POST':
        context = {}
        return render(request, 'attendance_sys/home.html', context)

    details = {
        'branch': request.POST['branch'],
        'year': request.POST['year'],
        'section': request.POST['section'],
        'period': request.POST['period'],
        'faculty': request.POST['branch'],
    }

    today = str(date.today())
    branch = details['branch']
    year = details['year']
    section = details['section']
    period = details['period']
    faculty = details['faculty']

    objects = Attendance.objects.filter(
        date=today,
        branch=branch,
        year=year,
        section=section,
        period=period,
    )

    if objects.count() != 0:
        messages.error(request, "attendance already recorded.")
        return redirect('home')

    students = Student.objects.filter(
        branch=branch,
        year=year,
        section=section,
    )
    names = recognizer(details)

    for student in students:
        reg_id = str(student.registration_id)

        attendance = Attendance(
            Faculty_Name=faculty,
            Student_ID=reg_id,
            period=period,
            branch=branch,
            year=year,
            section=section,
        )

        if names is not None and reg_id in names:
            attendance.status = 'Present'

        attendance.save()

    attendances = Attendance.objects.filter(
        date=today,
        branch=branch,
        year=year,
        section=section,
        period=period,
    )

    context = {"attendances": attendances, "ta": True}
    messages.success(request, "attendance taking Success")
    return render(request, 'attendance_sys/attendance.html', context)


def search_attendance(request):
    attendances = Attendance.objects.all()
    myFilter = AttendanceFilter(request.GET, queryset=attendances)
    attendances = myFilter.qs
    context = {'myFilter': myFilter, 'attendances': attendances, 'ta': False}
    return render(request, 'attendance_sys/attendance.html', context)
