from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    instructor = models.CharField(max_length=100)
    credits = models.IntegerField(default=3)
    schedule = models.CharField(max_length=200, help_text="e.g., Mon/Wed/Fri 10:00-11:00")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        ordering = ['code']

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    courses = models.ManyToManyField(Course, blank=True, related_name='enrolled_students')
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"
    
    def get_gpa(self):
        grades = Grade.objects.filter(student=self)
        if not grades:
            return 0.0
        total_points = sum(grade.get_grade_points() * grade.course.credits for grade in grades)
        total_credits = sum(grade.course.credits for grade in grades)
        return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

class Grade(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+ (4.0)'),
        ('A', 'A (4.0)'),
        ('A-', 'A- (3.7)'),
        ('B+', 'B+ (3.3)'),
        ('B', 'B (3.0)'),
        ('B-', 'B- (2.7)'),
        ('C+', 'C+ (2.3)'),
        ('C', 'C (2.0)'),
        ('C-', 'C- (1.7)'),
        ('D+', 'D+ (1.3)'),
        ('D', 'D (1.0)'),
        ('F', 'F (0.0)'),
    ]
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
    assignment_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    exam_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    final_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_grade_points(self):
        grade_points = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'F': 0.0
        }
        return grade_points.get(self.grade, 0.0)
    
    def save(self, *args, **kwargs):
        # Auto-calculate final score and grade
        self.final_score = (self.assignment_score * 0.4) + (self.exam_score * 0.6)
        
        if self.final_score >= 97:
            self.grade = 'A+'
        elif self.final_score >= 93:
            self.grade = 'A'
        elif self.final_score >= 90:
            self.grade = 'A-'
        elif self.final_score >= 87:
            self.grade = 'B+'
        elif self.final_score >= 83:
            self.grade = 'B'
        elif self.final_score >= 80:
            self.grade = 'B-'
        elif self.final_score >= 77:
            self.grade = 'C+'
        elif self.final_score >= 73:
            self.grade = 'C'
        elif self.final_score >= 70:
            self.grade = 'C-'
        elif self.final_score >= 67:
            self.grade = 'D+'
        elif self.final_score >= 60:
            self.grade = 'D'
        else:
            self.grade = 'F'
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.code} - {self.grade}"
    
    class Meta:
        unique_together = ['student', 'course']

class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    remarks = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student.user.get_full_name()} - {self.course.code} - {self.date} - {status}"
    
    class Meta:
        unique_together = ['student', 'course', 'date']
        ordering = ['-date']

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('exam', 'Exam'),
        ('assignment', 'Assignment'),
        ('announcement', 'Announcement'),
        ('grade', 'Grade Update'),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    recipients = models.ManyToManyField(StudentProfile, blank=True)
    is_global = models.BooleanField(default=False, help_text="Send to all students")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_notification_type_display()}"
    
    class Meta:
        ordering = ['-created_at']
