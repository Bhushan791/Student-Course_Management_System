from django.contrib.auth.models import User
from .models import Course, StudentProfile, Grade, Attendance, Notification
from datetime import date, datetime, timedelta
import random

def create_sample_data():
    """
    Create sample data for the Student Management System
    Run this in Django shell: exec(open('home/sample_data.py').read())
    """
    print("Creating sample data for Student Management System...")

    # Create sample courses with Nepali instructor names
    courses_data = [
        {
            'name': 'Introduction to Computer Science',
            'code': 'CS101',
            'description': 'Basic concepts of computer science, programming fundamentals, and problem-solving techniques.',
            'instructor': 'Dr. Suman Adhikari',
            'credits': 3,
            'schedule': 'Mon/Wed/Fri 9:00-10:00 AM'
        },
        {
            'name': 'Calculus I',
            'code': 'MATH101',
            'description': 'Differential and integral calculus with applications to science and engineering.',
            'instructor': 'Prof. Nirmala Sharma',
            'credits': 4,
            'schedule': 'Tue/Thu 10:30-12:00 PM'
        },
        {
            'name': 'English Composition',
            'code': 'ENG101',
            'description': 'Academic writing, research methods, and composition skills for college-level work.',
            'instructor': 'Dr. Ravi Shrestha',
            'credits': 3,
            'schedule': 'Mon/Wed 2:00-3:30 PM'
        },
        {
            'name': 'Physics I',
            'code': 'PHYS101',
            'description': 'Classical mechanics, thermodynamics, and wave phenomena with laboratory work.',
            'instructor': 'Dr. Kabita Bista',
            'credits': 4,
            'schedule': 'Tue/Thu 1:00-2:30 PM'
        },
        {
            'name': 'Data Structures and Algorithms',
            'code': 'CS201',
            'description': 'Advanced data structures, algorithm analysis, and programming techniques.',
            'instructor': 'Dr. Prakash Gautam',
            'credits': 3,
            'schedule': 'Mon/Wed/Fri 11:00-12:00 PM'
        },
        {
            'name': 'Statistics',
            'code': 'MATH201',
            'description': 'Probability theory, statistical inference, and data analysis methods.',
            'instructor': 'Prof. Laxmi Karki',
            'credits': 3,
            'schedule': 'Tue/Thu 9:00-10:30 AM'
        }
    ]

    # Create courses
    created_courses = []
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            code=course_data['code'],
            defaults=course_data
        )
        created_courses.append(course)
        if created:
            print(f"✓ Created course: {course.code} - {course.name}")
        else:
            print(f"- Course already exists: {course.code}")

    # Create sample notifications (no instructor names here, but you can Nepali-style titles)
    notifications_data = [
        {
            'title': 'Midterm Exam Schedule Released',
            'message': 'Midterm pariksha ko talika chhapa bhaeko chha. Kripaya portal ma check garnuhos.',
            'notification_type': 'exam',
            'is_global': True
        },
        {
            'title': 'Library Hours Extended During Finals',
            'message': 'Antim pariksha ko samaya ma library 24 ghanta khula rahanechha.',
            'notification_type': 'announcement',
            'is_global': True
        },
        {
            'title': 'Programming Assignment Due Soon',
            'message': 'Yaad garaun: CS101 ko assignment yo Friday 11:59 PM samma submit garnu parcha.',
            'notification_type': 'assignment',
            'course': Course.objects.filter(code='CS101').first(),
            'is_global': False
        },
        {
            'title': 'Grade Updates Available',
            'message': 'Tapaiko latest assignment ra quiz ko grade update bhayeko chha.',
            'notification_type': 'grade',
            'is_global': True
        },
        {
            'title': 'Campus WiFi Maintenance',
            'message': 'Yo Saturday 2:00AM-6:00AM samma WiFi maintenance huney chha.',
            'notification_type': 'announcement',
            'is_global': True
        }
    ]

    # Create notifications
    for notif_data in notifications_data:
        notification, created = Notification.objects.get_or_create(
            title=notif_data['title'],
            defaults=notif_data
        )
        if created:
            print(f"✓ Created notification: {notification.title}")
        else:
            print(f"- Notification already exists: {notification.title}")

    # Create sample student data if there are existing students
    students = StudentProfile.objects.all()
    if students.exists():
        print(f"\nFound {students.count()} existing students. Creating sample grades and attendance...")

        # Create sample grades for existing students
        for student in students[:3]:  # Limit to first 3 students
            enrolled_courses = student.courses.all()
            for course in enrolled_courses:
                if not Grade.objects.filter(student=student, course=course).exists():
                    assignment_score = random.uniform(75, 95)
                    exam_score = random.uniform(70, 98)

                    grade = Grade.objects.create(
                        student=student,
                        course=course,
                        assignment_score=assignment_score,
                        exam_score=exam_score
                    )
                    print(f"✓ Created grade: {student.user.get_full_name()} - {course.code} - {grade.grade}")

        # Create sample attendance records
        for student in students[:3]:
            enrolled_courses = student.courses.all()
            for course in enrolled_courses:
                for i in range(10):
                    attendance_date = date.today() - timedelta(days=i)
                    if attendance_date.weekday() < 5:  # Monday to Friday
                        if not Attendance.objects.filter(student=student, course=course, date=attendance_date).exists():
                            is_present = random.random() < 0.85
                            remarks = "" if is_present else random.choice(["Bimaar", "Dhilo", "Chhutti", ""])
                            Attendance.objects.create(
                                student=student,
                                course=course,
                                date=attendance_date,
                                is_present=is_present,
                                remarks=remarks
                            )
                print(f"✓ Created attendance records for {student.user.get_full_name()} - {course.code}")

    print("\n" + "="*50)
    print("SAMPLE DATA CREATION COMPLETE!")
    print("="*50)
    print("\nSummary:")
    print(f"📚 Courses: {Course.objects.count()}")
    print(f"👥 Students: {StudentProfile.objects.count()}")
    print(f"📊 Grades: {Grade.objects.count()}")
    print(f"📅 Attendance Records: {Attendance.objects.count()}")
    print(f"🔔 Notifications: {Notification.objects.count()}")

    print("\nNext Steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Start the server: python manage.py runserver")
    print("3. Access admin panel: http://127.0.0.1:8000/admin/")
    print("4. Register students: http://127.0.0.1:8000/register/")
    print("5. Login as student: http://127.0.0.1:8000/login/")

    print("\nAdmin Panel Features:")
    print("- Manage students and courses")
    print("- Enter grades and attendance")
    print("- Send notifications")
    print("- Generate reports")

if __name__ == '__main__':
    create_sample_data()
