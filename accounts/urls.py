from django.urls import path


from . import views as vi


app_name = "accounts"

urlpatterns = [
    path('',vi.user_login,name='login'),
    path('logout',vi.logout_user,name='logout'),
    # ====================== Admin urls ====================================
    path('admin-dashboard',vi.admin_dashboard,name='admin_dashboard'),
    path('admin-profile',vi.admin_profile,name='admin_profile'),
    path('admin-view/student',vi.admin_view_students,name='view_student'),
    path('admin-registration',vi.admin_registration,name='admin_registeration'),

    # ====================== student urls ===========================
    path('student-registration',vi.student_registration,name='student_registeration'),
    path('student-profile',vi.student_profile,name="student_profile"), 
    path('student-dashboard',vi.student_dashboard,name='student_dashboard'), 
]