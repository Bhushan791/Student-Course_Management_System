from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Course, StudentProfile, Grade, Attendance, Notification

# Unregister the default User admin
admin.site.unregister(User)

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (StudentProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_student_id')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    def get_student_id(self, obj):
        try:
            return obj.studentprofile.student_id
        except:
            return 'N/A'
    get_student_id.short_description = 'Student ID'

admin.site.register(User, CustomUserAdmin)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'instructor', 'credits', 'get_enrolled_count')
    list_filter = ('instructor', 'credits')
    search_fields = ('code', 'name', 'instructor')
    ordering = ('code',)
    
    def get_enrolled_count(self, obj):
        return obj.enrolled_students.count()
    get_enrolled_count.short_description = 'Enrolled Students'

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'get_full_name', 'get_email', 'enrollment_date', 'get_gpa')
    list_filter = ('enrollment_date', 'courses')
    search_fields = ('student_id', 'user__first_name', 'user__last_name', 'user__email')
    filter_horizontal = ('courses',)
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'grade', 'assignment_score', 'exam_score', 'final_score')
    list_filter = ('grade', 'course', 'created_at')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'course__code')
    ordering = ('-created_at',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'is_present', 'remarks')
    list_filter = ('is_present', 'course', 'date')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'course__code')
    ordering = ('-date',)
    date_hierarchy = 'date'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'course', 'is_global', 'created_at')
    list_filter = ('notification_type', 'is_global', 'course', 'created_at')
    search_fields = ('title', 'message')
    filter_horizontal = ('recipients',)
    ordering = ('-created_at',)

# Customize admin site headers
admin.site.site_header = "Student Management System"
admin.site.site_title = "SMS Admin"
admin.site.index_title = "Welcome to Student Management System Administration"
