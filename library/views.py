from django.shortcuts import render,redirect,get_object_or_404

from . import models as mdl
from . import forms as fms
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


def books(request):
    '''all books in the system'''
    context = {}
    return render(request,'library/books.html',context)

def add_book(request):
    '''add book into the system'''
    if request.method == 'POST':
        form = fms.BookCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:add_book')
    else:
        form = fms.BookCreationForm()
    context = {'form':form}
    return render(request,'library/add_books.html',context)


def view_shelve_books(request,shelve_id):
    context = {}
    return render(request,'library/view_shelve_books.html',context)

def issue_book(request):
    '''lend book to student'''
    context = {}
    return render(request, 'library/issue_book.html',context)

def view_issued_books(request):
    '''view lended books'''
    context = {}
    return render(request,'library/view_issued_books.html',context)

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
    context = {}
    return render(request,'library/edit_shelve.html',context)

def edit_book(request,book_id):
    context = {}
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
    return redirect('library:library_books')