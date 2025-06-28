# 🎓✨ Student Management System ✨🎓  
### 📚 Course Project Assignment | Powered by Django & Bootstrap 🚀

---

## 🚀 **Project Overview** 🚀

Welcome to the **Student Management System**, a 💻 **Django-powered** web app designed to simplify academic life! Manage 👩‍🎓 students, 📘 courses, 📊 grades, and 🕒 attendance — all with a beautiful, responsive Bootstrap interface! 🎨

---

## 🎯 **Project Objectives** 🎯

- ✅ Build a full-featured academic management platform  
- 🔐 Secure authentication & role-based access (Students & Admins)  
- 🗄️ Efficient data handling with Django ORM  
- 📱 Mobile-friendly design with Bootstrap 5.3  
- 📈 Real-time grades, attendance, and notifications  

---

## 🌟 **Features** 🌟

### 👩‍🎓 Student Portal
- 📝 Register & login securely  
- 📊 Dashboard: Your grades, courses, & attendance at a glance  
- 📚 Browse & enroll in courses  
- 🎓 Track your GPA automatically  
- 📅 Attendance tracking with progress bars  
- 🔔 Stay informed with notifications & announcements  

### 👨‍💼 Admin Control Panel
- 👥 Manage students & profiles  
- 📋 Create & schedule courses with instructors  
- ✍️ Input grades & attendance  
- 📢 Send important notifications  
- 🔒 Full control via Django admin panel  

---

## ⚙️ **Technologies Used** ⚙️

- 🐍 Python 3.8+  
- 🌐 Django 5.2 Framework  
- 🎨 Bootstrap 5.3 + Font Awesome 6.4  
- 🗃️ SQLite database  
- 🧰 Git for version control  

---

## 🚦 **Setup & Installation** 🚦

```bash
# Clone repository
git clone https://github.com/Bhushan791/Student-Course_Management_System.git
cd StudentManagement

# Create & activate virtual environment
python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate

# Install Django
pip install django

# Setup database
python manage.py makemigrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Load sample data with fun Nepali names 🎉
python manage.py shell
>>> from home.sample_data import create_sample_data
>>> create_sample_data()
>>> exit()

# Start your development server
python manage.py runserver
