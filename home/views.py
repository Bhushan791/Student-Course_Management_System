from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Avg, Count
from django.http import JsonResponse
from .models import Course, StudentProfile, Grade, Attendance, Notification
from .forms import StudentRegistrationForm, StudentProfileForm

def home(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'studentprofile'):
            return redirect('student_dashboard')
        else:
            return redirect('admin:index')
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create student profile
            student_profile = StudentProfile.objects.create(
                user=user,
                student_id=form.cleaned_data['student_id'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                date_of_birth=form.cleaned_data['date_of_birth']
            )
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('student_dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def student_dashboard(request):
    try:
        student_profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found. Please contact admin.')
        return redirect('home')
    
    # Get enrolled courses
    enrolled_courses = student_profile.courses.all()
    
    # Get recent grades
    recent_grades = Grade.objects.filter(student=student_profile).order_by('-created_at')[:5]
    
    # Get recent notifications
    notifications = Notification.objects.filter(
        recipients=student_profile
    ).order_by('-created_at')[:5]
    
    # Get global notifications
    global_notifications = Notification.objects.filter(
        is_global=True
    ).order_by('-created_at')[:3]
    
    # Combine notifications
    all_notifications = list(notifications) + list(global_notifications)
    all_notifications.sort(key=lambda x: x.created_at, reverse=True)
    all_notifications = all_notifications[:5]
    
    # Calculate attendance percentage for each course
    attendance_data = []
    for course in enrolled_courses:
        total_classes = Attendance.objects.filter(student=student_profile, course=course).count()
        present_classes = Attendance.objects.filter(
            student=student_profile, 
            course=course, 
            is_present=True
        ).count()
        percentage = (present_classes / total_classes * 100) if total_classes > 0 else 0
        attendance_data.append({
            'course': course,
            'percentage': round(percentage, 1),
            'present': present_classes,
            'total': total_classes
        })
    
    context = {
        'student_profile': student_profile,
        'enrolled_courses': enrolled_courses,
        'recent_grades': recent_grades,
        'notifications': all_notifications,
        'attendance_data': attendance_data,
        'gpa': student_profile.get_gpa()
    }
    return render(request, 'student_dashboard.html', context)

@login_required
def profile(request):
    try:
        student_profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student_profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = StudentProfileForm(instance=student_profile, user=request.user)
    
    return render(request, 'profile.html', {'form': form, 'student_profile': student_profile})

@login_required
def courses(request):
    try:
        student_profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    available_courses = Course.objects.exclude(enrolled_students=student_profile)
    enrolled_courses = student_profile.courses.all()
    
    context = {
        'available_courses': available_courses,
        'enrolled_courses': enrolled_courses,
        'student_profile': student_profile
    }
    return render(request, 'courses.html', context)

@login_required
def enroll_course(request, course_id):
    try:
        student_profile = request.user.studentprofile
        course = get_object_or_404(Course, id=course_id)
        
        if course not in student_profile.courses.all():
            student_profile.courses.add(course)
            messages.success(request, f'Successfully enrolled in {course.name}!')
        else:
            messages.warning(request, f'You are already enrolled in {course.name}.')
            
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found.')
    
    return redirect('courses')

@login_required
def grades(request):
    try:
        student_profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    student_grades = Grade.objects.filter(student=student_profile).order_by('-created_at')
    
    context = {
        'grades': student_grades,
        'gpa': student_profile.get_gpa(),
        'student_profile': student_profile
    }
    return render(request, 'grades.html', context)

@login_required
def attendance(request):
    try:
        student_profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    # Get attendance records grouped by course
    enrolled_courses = student_profile.courses.all()
    attendance_data = []
    
    for course in enrolled_courses:
        attendance_records = Attendance.objects.filter(
            student=student_profile, 
            course=course
        ).order_by('-date')
        
        total_classes = attendance_records.count()
        present_classes = attendance_records.filter(is_present=True).count()
        percentage = (present_classes / total_classes * 100) if total_classes > 0 else 0
        
        attendance_data.append({
            'course': course,
            'records': attendance_records,
            'total_classes': total_classes,
            'present_classes': present_classes,
            'absent_classes': total_classes - present_classes,
            'percentage': round(percentage, 1)
        })
    
    context = {
        'attendance_data': attendance_data,
        'student_profile': student_profile
    }
    return render(request, 'attendance.html', context)

@login_required
def notifications(request):
    try:
        student_profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    # Get personal notifications
    personal_notifications = Notification.objects.filter(
        recipients=student_profile
    ).order_by('-created_at')
    
    # Get global notifications
    global_notifications = Notification.objects.filter(
        is_global=True
    ).order_by('-created_at')
    
    context = {
        'personal_notifications': personal_notifications,
        'global_notifications': global_notifications,
        'student_profile': student_profile
    }
    return render(request, 'notifications.html', context)
