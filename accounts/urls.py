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
    path('delete-user/<user_id>',vi.delete_user,name="delete-user"),
    path('admin-registration',vi.admin_registration,name='admin_registeration'),

    # ====================== student urls ===========================
    path('user-registration',vi.student_registration,name='student_registeration'),
    path('profile/<int:user_id>',vi.user_profile,name="user_profile"), 
    path('student-dashboard',vi.student_dashboard,name='student_dashboard'), 
    # ===================================== student accounts on the system ============
    path('show-library/books',vi.library_books,name='library-books'), 
    path('request-book/<int:book_id>',vi.request_a_book,name='request_book'),
    path('disable-my-request/<int:book_id>',vi.disable_my_book_request,name='disable_request'),
    path('my-borrowed/books',vi.my_borrowed_books,name='my-borrowed-books'), 
    path('my-read/books',vi.my_read_books,name='my-read-books'), 
    path('my-returned/books',vi.my_returned_books,name='my-returned-books'), 
    path('return-a/book/<int:book_id>',vi.return_a_book,name='return-book'),
    path('my-request/books',vi.my_requested_books,name='my-requested-books'),
]