from django.shortcuts import render,redirect,get_object_or_404
from django.utils.timezone import now

from . import models as mdl
from . import forms as fms
from accounts import models as acmdl
# Create your views here.

def index(request):
    ''' front page of the site'''
    context = {}
    return render(request,'library/index.html',context)

def shelves(request):
    library_shelves = mdl.Shelve.objects.order_by('-date_updated').all()
    if request.method == 'POST':
        form = fms.ShelveCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library:shelves')
    else:
        form = fms.ShelveCreationForm()
    context = {'form':form,'shelves':library_shelves}
    return render(request,'library/shelves.html',context)

def create_shelve(request):
    if request.method == 'POST':
        form = fms.ShelveCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library:create_shelve')
    else:
        form = fms.ShelveCreationForm()
    context = {'form':form}
    return render(request,'library/create_shelve.html',context)


def books(request):
    '''all books in the system'''
    books = mdl.Book.objects.order_by('-date_updated').all()
    context = {'books':books}
    return render(request,'library/books.html',context)

def add_new_book(request):
    '''add book into the system'''
    admin = get_object_or_404(acmdl.Administrator,user=request.user)
    books = mdl.Book.objects.order_by('-date_updated').all()
    if request.method == 'POST':
        form = fms.BookCreationForm(request.POST,request.FILES)
        if form.is_valid():
            new_book = form.save(commit=False)
            new_book.admin = admin
            new_book.save()
            return redirect('library:add_book')
    else:
        form = fms.BookCreationForm()
    context = {'form':form,'books':books}
    return render(request,'library/add_books.html',context)


def view_shelve_books(request,shelve_id):
    context = {}
    return render(request,'library/view_shelve_books.html',context)

def view_shelve_details(request,shelve_id):
    shelve = get_object_or_404(mdl.Shelve,id=shelve_id)
    context = {'shelve':shelve,'now':now()}
    return render(request,'library/view_shelve_details.html',context)

def view_book_details(request,book_id):
    book = get_object_or_404(mdl.Book,id=book_id)
    context = {'book':book}
    return render(request,'library/view_book_details.html',context)

def view_requested_book(request):
    '''lend book to student'''
    requested_books = mdl.Requestedbook.objects.filter(request_book=True,issue_book=False).all()
    context = {'requsted_books':requested_books}
    return render(request, 'library/issue_book.html',context)

def issue_book(request,book_id,borrower_id):
    requested_book = get_object_or_404(mdl.Requestedbook,id=book_id,requested_user=borrower_id)
    issued_book = mdl.Borrowedbook(book=requested_book.book,
    borrower=acmdl.User.objects.get(id=borrower_id)
    )
    requested_book.issue_book = True
    requested_book.request_book = False
    issued_book.save()
    requested_book.save()
    return redirect('library:requested_book')

def view_issued_books(request):
    '''view lended books'''
    issued_books = mdl.Requestedbook.objects.filter(request_book=False,issue_book=True).all()
    context = {'issued_books':issued_books}
    return render(request,'library/view_issued_books.html',context)

def view_returned_books(request):
    returned_books = mdl.Borrowedbook.objects.order_by('-date_returned').filter(book_returned=True).all()
    context = {'returned_books':returned_books}
    return render(request,'library/view_returned_books.html',context)

def confirm_returned_book(request,book_id):
    borrowed_book = get_object_or_404(mdl.Borrowedbook,id=book_id,confirm_returned_book=False,book_returned=True)
    if borrowed_book.book_returned:
        borrowed_book.confirm_returned_book = True
        borrowed_book.book.number_in_stock += 1
        borrowed_book.save()
    return redirect('library:returned_books')
    


def mybooks(request):
    '''student viewing their borrowed books'''
    context = {}
    return render(request,'accounts/student_site/mybooks.html',context)

def expired_books(request):
    '''system showing lend but none returned books'''
    context = {}
    return render(request, 'accounts/student_site/expired_none_return_book.html',context)

# =============================== Edit actions =======================
def edit_shelve(request,shelve_id):
    shelve = get_object_or_404(mdl.Shelve,id=shelve_id)
    admin = get_object_or_404(acmdl.Administrator,user=request.user)
    if request.method == 'POST':
        form = fms.ShelveCreationForm(instance=shelve,data=request.POST)
        if form.is_valid():
            edit_new_book = form.save(commit=False)
            edit_new_book.admin = admin
            edit_new_book.save()
            return redirect('library:shelves')
    else:
        form = fms.ShelveCreationForm(instance=shelve)
    context = {'shelve':shelve,'form':form}
    return render(request,'library/edit_shelve.html',context)

def edit_book(request,book_id):
    book = get_object_or_404(mdl.Book,id=book_id)
    admin = get_object_or_404(acmdl.Administrator,user=request.user)
    if request.method == 'POST':
        form = fms.BookCreationForm(instance=book,data=request.POST,files=request.FILES)
        if form.is_valid():
            edit_new_book = form.save(commit=False)
            edit_new_book.admin = admin
            edit_new_book.save()
            return redirect('library:add_book')
    else:
        form = fms.BookCreationForm(instance=book)
    context = {'book':book,'form':form}
    return render(request,'library/edit_book.html',context)

# ======================== delete actions =============================
def delete_shelve(request,shelve_id):
    shelve = get_object_or_404(mdl.Shelve,id=shelve_id)
    try:
        shelve.delete()
    except Exception as e:
        print(f'Operation failed due to {e}')
    return redirect('library:shelves')

def delete_book(request,book_id):
    book = get_object_or_404(mdl.Book,id=book_id)
    try:
        book.delete()
    except Exception as e:
        print(f'Operation failed due to {e}')
    return redirect('library:library_books')