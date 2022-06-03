from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
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
                if get_object_or_404(mdl.Administrator,user=request.user):
                    return redirect('accounts:admin_dashboard')
                else:
                    return redirect('accounts:student_dashboard')
    else:
        form = fms.LoginUserForm()
    context = {'form':form}
    return render(request, 'accounts/login.html',context)

def logout_user(request):
    logout(request)
    return redirect('accounts:login')
# ================================ admin site ===================

def admin_dashboard(request):
    total_books = lmdl.Book.objects.count()
    borrowed_books = lmdl.Book.objects.filter(issue_book=True).count()
    returned_books = lmdl.Book.objects.filter(book_returned=True).count()
    total_shelves = lmdl.Shelve.objects.count()
    books = lmdl.Book.objects.order_by('-date_updated').all()
    context = {
        'total_books':total_books,
        'total_shelves':total_shelves,
        'borrowed_books':borrowed_books,
        'no_returned_books':borrowed_books-returned_books,
        'books':books,
        }
    return render(request,'accounts/admin_site/dashboard.html',context)


def admin_profile(request):
    context = {}
    return render(request,'accounts/admin_site/profile.html',context)

def admin_view_students(request):
    context = {}
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
# ============================== student site ================================

def student_registration(request):
    if request.method == "POST":
        form = fms.StudentRegisterationForm(request.POST)
        if form.is_valid():
            form.is_student = True
            form.save()
            return redirect('accounts:login')
    else:
        form = fms.StudentRegisterationForm()
    context = {'form':form}
    return render(request, 'accounts/student_site/registration.html',context)

def student_profile(request):
    context = {}
    return render(request,'accounts/student_site/profile.html',context)

def student_dashboard(request):
    context = {}
    return render(request,'accounts/student_site/dashboard.html',context)