from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('courses/', views.courses, name='courses'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('grades/', views.grades, name='grades'),
    path('attendance/', views.attendance, name='attendance'),
    path('notifications/', views.notifications, name='notifications'),
]
