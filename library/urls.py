from django.urls import path

from . import views as vi 

app_name = 'library'


urlpatterns = [
    path('home',vi.index,name='home'),
    # =================== library urls =================== 
    path('shelves',vi.shelves,name='shelves'),
    path('create-shelve',vi.create_shelve,name='create_shelve'),
    path('view-shelve/<int:shelve_id>/details',vi.view_shelve_details,name='shelve_details'),
    path('library-books',vi.books,name='library_books'),
    path('add-book',vi.add_new_book,name='add_book'),
    path('view-book/<int:book_id>/details',vi.view_book_details,name='book_details'),
    path('issue-book',vi.issue_book,name='issue_book'),
    path('view/issue-books',vi.view_issued_books,name='view_issue_books'),
    path('student-books',vi.mybooks,name="mybooks"), 
    path('student/expired-books',vi.expired_books,name="expired_books"),
    path('view-shelve-books/<int:shelve_id>',vi.view_shelve_books,name='view_shelve_books'),
    # ========================= edit ====================================
    path('edit-shelve/<int:shelve_id>',vi.edit_shelve,name='edit_shelve'),
    path('edit-book/<int:book_id>',vi.edit_book,name='edit_book'),
    path('delete-shelve/<int:shelve_id>',vi.delete_shelve,name='delete_shelve'),
    path('delete-book/<int:book_id>',vi.delete_book,name='delete_book'),
]