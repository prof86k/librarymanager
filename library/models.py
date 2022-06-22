from tabnanny import verbose
from django.db import models
from accounts import models as acmdl

# Create your models here.

class Shelve(models.Model):
    shelve_name = models.CharField(verbose_name='shelve Name',max_length=255,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        verbose_name = 'Shelve'
        verbose_name_plural = "Shelves"


    def __str__(self):
        return self.shelve_name


class Book(models.Model):
    shelve = models.ForeignKey(Shelve,on_delete=models.CASCADE,related_name='shelve_book')
    admin = models.ForeignKey(acmdl.Administrator,on_delete=models.PROTECT)
    title = models.CharField(verbose_name="Title:",max_length=255,null=True)
    author = models.CharField(verbose_name="Author:",max_length=255,null=True)
    co_author = models.CharField(verbose_name="Co-Authors:",max_length=255,null=True)
    image = models.ImageField(verbose_name='Book Image:',upload_to='images/%Y/%m/%d')
    book_pdf = models.FileField(verbose_name='Book PDF:',upload_to='books/pdf/%Y/%m/%d')
    book_edition = models.CharField(verbose_name='Edition:',max_length=255,null=True)
    pub_year = models.DateField(verbose_name="Publication Year:",null=True)
    number_in_stock = models.PositiveIntegerField(verbose_name='No. in Stock',null=True,blank=True)
    pub_by = models.CharField(verbose_name='Publish By:',max_length=255,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_to_return = models.DateField(verbose_name='Date to Return',null=True)

    class Meta:
        managed = True
        verbose_name = 'Book'
        verbose_name_plural = "Books"

    def __str__(self) -> str:
        return self.title

    def uploaded_by(self):
        return self.admin.user.username

    def is_avaliable(self):
        if self.number_in_stock > 0:
            return True
        return False

class Borrowedbook(models.Model):
    book = models.ForeignKey(Book,on_delete=models.PROTECT,related_name='my_borrowed_books')
    borrower = models.ForeignKey(acmdl.User,on_delete=models.PROTECT,related_name='book_borrowers')
    date_borrowed = models.DateTimeField(auto_now_add=True)
    book_returned = models.BooleanField(default=False)
    confirm_returned_book = models.BooleanField(default=False)
    date_returned = models.DateField(null=True)
    
    class Meta:
        managed = True
        verbose_name = 'Borrowed Book'
        verbose_name_plural = 'Borrowed Books'

    def borrowed_by(self):
        '''return the current user of the book'''
        return self.borrower.username

    def returned_by(self):
        '''return the user who returned the book'''
        return self.borrower.username

    def over_due_non_returned_books(self):
        '''user does not return the book on or before the due date'''
        book_settings = Booksettings.objects.first()
        if book_settings and (book_settings.date_to_return < self.date_returned):
            return True
        return False

    def __str__(self) -> str:
        return self.book.title


class Booksettings(models.Model):
    max_books_to_borrow = models.PositiveIntegerField(verbose_name='Max Books to Borrow:',null=True,blank=True)
    fine_amount = models.DecimalField(verbose_name='Fine Amount:',decimal_places=2,max_digits=20,null=True,blank=True)
    fine_to = models.ForeignKey(acmdl.User,on_delete=models.PROTECT,related_name='fine_people')
    date_to_return = models.DateField(verbose_name='Date to Return',null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'

    def __str__(self) -> str:
        return 'Settings'


class Requestedbook(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='requested_books')
    requested_user = models.ForeignKey(acmdl.User,on_delete=models.PROTECT)
    issue_book = models.BooleanField(verbose_name="Issued:",default=False)
    request_book = models.BooleanField(verbose_name="Request Book:",default=False)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        verbose_name = 'Requested Book'
        verbose_name_plural = 'Requested Books'

    def __str__(self) -> str:
        return f'{self.requested_user} {self.book}'