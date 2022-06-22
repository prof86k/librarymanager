from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils import timezone

from library.views import confirm_returned_book
from . import forms as fms
from . import models as mdl
from library import models as lmdl

# Create your views here.
# ============= login page ===================================
def user_login(request):
    if request.method == 'POST':
        form = fms.LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user=user)
                if get_object_or_404(mdl.User,username=request.user).is_administrator:
                    return redirect('accounts:admin_dashboard')
                else:
                    return redirect('accounts:student_dashboard')
            else:
                messages.error(request,"User or Password Invalid!")
    else:
        form = fms.LoginUserForm()
    context = {'form':form}
    return render(request, 'accounts/login.html',context)

def logout_user(request):
    logout(request)
    messages.info(request,'You have successfully logged out. Login again anytime to access your dashboard')
    return redirect('accounts:login')
# ================================ admin site ===================

def admin_dashboard(request):
    total_books = lmdl.Book.objects.count()
    borrowed_books = lmdl.Requestedbook.objects.filter(issue_book=True).count()
    returned_books = lmdl.Borrowedbook.objects.filter(book_returned=True).count()
    total_shelves = lmdl.Shelve.objects.count()
    books = lmdl.Book.objects.order_by('-date_updated').all()
    context = {
        'total_books':total_books,
        'total_shelves':total_shelves,
        'borrowed_books':borrowed_books,
        'no_returned_books':returned_books,
        'books':books,
        }
    # for book in lmdl.Borrowedbook.objects.all():
        # book.delete()
    # for book in lmdl.Requestedbook.objects.all():
        # book.delete()
    return render(request,'accounts/admin_site/dashboard.html',context)


def admin_profile(request):
    context = {}
    return render(request,'accounts/admin_site/profile.html',context)

def admin_view_students(request):
    system_users = mdl.User.objects.filter(is_student=True).all()
    context = {'users':system_users}
    return render(request,'accounts/admin_site/view_students.html',context)

def admin_registration(request):
    if request.method == "POST":
        form = fms.AdministratorRegisterationForm(request.POST)
        if form.is_valid():
            request.user.is_administrator = True
            form.save()
            return redirect('accounts:login')
    else:
        form = fms.AdministratorRegisterationForm()
    context = {'form':form}
    return render(request, 'accounts/registration.html',context)

def delete_user(request,user_id):
    user = get_object_or_404(mdl.User,id=user_id)
    user.delete()
    return redirect('accounts:view_student')
# ============================== student site ================================

def student_registration(request):
    user_password = 'library2022'
    if request.method == "POST":
        form = fms.createNewUserForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            new_user_id = form.cleaned_data.get('username')
            user_is_admin = form.cleaned_data.get('is_admin')
            user_is_student = form.cleaned_data.get('is_student')
            new_user = mdl.User(username=new_user_id,email=user_email,is_administrator=user_is_admin,is_student=user_is_student)
            try:
                new_user.set_password(user_password)
                new_user.save()
                if new_user.is_student:
                    student = mdl.Student.objects.create(user=new_user)
                else:
                    admin = mdl.Administrator.objects.create(user=new_user)
                return redirect('accounts:view_student')
            except Exception as e:
                print(f'unable to save the new user {e}')
    else:
        form = fms.createNewUserForm()
        # print(form.error_messages)
    context = {'form':form}
    return render(request, 'accounts/admin_site/register_new_student.html',context)

def user_profile(request,user_id):
    user_profile = get_object_or_404(mdl.User,id=user_id)
    # student_user = get_object_or_404(mdl.Student,user=user_profile)
    if request.method == "POST":
        form = fms.UserProfileForm(instance=user_profile,data=request.POST,files=request.FILES)
        if form.is_valid():
            full_name = form.cleaned_data.get('full_name')
            student_email = form.cleaned_data.get('email')
            student_gender = form.cleaned_data.get('gender')
            pic = form.cleaned_data.get('profile_picture')
            user_profile.full_name = full_name
            user_profile.email = student_email
            user_profile.gender = student_gender
            user_profile.profile_picture = pic
            user_profile.save()
            messages.success(request,'Requested Updated successfully!')
            return redirect('accounts:user_profile',user_id=user_profile.id)
        else:
            messages.error(request,'Error: Resquested updates unsuccessfull.')
            return redirect('accounts:student_profile')

    else:
        form = fms.UserProfileForm(instance=user_profile)
    context = {'form':form,}
    return render(request,'accounts/student_site/profile.html',context)

def student_dashboard(request):
    library_books = lmdl.Book.objects.count()
    my_book = lmdl.Borrowedbook.objects.filter(book_returned=False,borrower=request.user).count()
    my_return_books = lmdl.Borrowedbook.objects.filter(borrower=request.user,book_returned=True,confirm_returned_book=True).count()
    over_due_books = lmdl.Borrowedbook.objects.filter(borrower=request.user).all()
    over_due = 0
    for book in over_due_books:
        if book.over_due_non_returned_books():
            over_due += 1
    context = {
        'library_books':library_books,
        'my_books':my_book,
        'return_books':my_return_books,
        'over_due_book':over_due,
    }
    return render(request,'accounts/student_site/dashboard.html',context)

def library_books(request):
    avaliable_books = lmdl.Book.objects.order_by('-date_updated').all()
    context = {'books':avaliable_books}
    return render(request,'accounts/student_site/library_books.html',context)

def my_borrowed_books(request):
    my_books = lmdl.Borrowedbook.objects.order_by('-book_returned').filter(borrower=request.user).all()
    context = {'my_books':my_books}
    return render(request,'accounts/student_site/my_borrowed_books.html',context)

def my_read_books(request):
    read_books = lmdl.Borrowedbook.objects.order_by('-date_returned').filter(borrower=request.user,book_returned=True).all()
    context = {'read_books':read_books}
    return render(request,'accounts/student_site/my_read_books.html',context)

def my_returned_books(request):
    returned_books = lmdl.Borrowedbook.objects.filter(borrower=request.user,book_returned=True,confirm_returned_book=True).all()
    context = {'returned_books':returned_books}
    return render(request,'accounts/student_site/my_returned_books.html',context)

def return_a_book(request,book_id):
    my_borrowed_book = get_object_or_404(lmdl.Borrowedbook,id=book_id,borrower=request.user)
    my_borrowed_book.book_returned = True
    my_borrowed_book.date_returned = timezone.now()
    my_borrowed_book.save()
    return redirect('accounts:my-borrowed-books')

def request_a_book(request,book_id):
    book = get_object_or_404(lmdl.Book,id=book_id)
    if book.is_avaliable():
        if (lmdl.Requestedbook.objects.filter(book=book,requested_user=request.user,request_book=True)).first() is None:
            save_requested_book(book=book,user=request.user)
            messages.success(request,'Your Request For The Book Was Successful.')
            return redirect('accounts:library-books')
        else:
            messages.error(request,'You Cannot Request A More Than Once.')
            return redirect('accounts:library-books')
    else:
        messages.error(request,'The Book You Request Is Not Avaliable At The Moment.')
        return redirect('accounts:library-books')

def save_requested_book(book,user):
    lmdl.Requestedbook.objects.create(book=book,requested_user=user,request_book=True)
    book.number_in_stock -= 1
    book.save()

def disable_my_book_request(request,book_id):
    requested_book = get_object_or_404(lmdl.Requestedbook,id=book_id,requested_user=request.user)
    requested_book.request_book = False
    requested_book.book.number_in_stock += 1
    requested_book.book.save()
    requested_book.delete()
    messages.success(request,'Request For Book Has Been Cancelled!')
    return redirect('accounts:my-requested-books')

def my_requested_books(request):
    my_books = lmdl.Requestedbook.objects.filter(requested_user=request.user,request_book=True).all()
    context = {'my_books':my_books}
    return render(request,'accounts/student_site/my_requested_books.html',context)

def my_overdue_books(request):
    overs = lmdl.Borrowedbook.objects.filter(borrower=request.user).all()
    context = {'overs':overs}
    return render(request,'accounts/student_site/my_overdue_books.html',context)