from django.db import models
from accounts import models as acmdl

# Create your models here.

class Shelve(models.Model):
    shelve_name = models.CharField(verbose_name='shelve Name',max_length=255,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
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
    pub_by = models.CharField(verbose_name='Publish By:',max_length=255,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    issue_book = models.BooleanField(verbose_name="Issued:",default=False)
    book_returned = models.BooleanField(verbose_name="Book Returned:",default=False)

    class Meta:
        verbose_name_plural = "Books"

    def __str__(self) -> str:
        return self.title

    def uploaded_by(self):
        return self.admin.user.username

    def loaned_by(self):
        self.issue_book = True
        self.book_returned = False
        self.student.user.username
        self.save()

    def returned_by(self):
        self.book_returned = True
        self.issue_book = False
        self.student.user.username
        self.save()

