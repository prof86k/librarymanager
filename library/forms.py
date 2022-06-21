from django import forms
from . import models as mdl 


class ShelveCreationForm(forms.ModelForm):
    class Meta:
        model = mdl.Shelve
        fields = ['shelve_name',]
        widgets = {
            'shelve_name':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Enter shelve name... eg. Mathematics Books',
                'required':True,
            }),
        }


class BookCreationForm(forms.ModelForm):
    class Meta:
        model = mdl.Book

        fields = ['shelve','title','author',
        'co_author','image','book_pdf','book_edition',
        'pub_year','pub_by','number_in_stock']

        widgets = {
            'shelve':forms.Select(attrs={
                'class':'form-control nice_Select2 nice_Select_line wide','required':True,
            }),
            'title':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Enter book title ...',
                'required':True,
            }),
            'author':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Enter book\'s author name...',
                'required':True,
            }),
            'co_author':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Enter Co-Authors (optional)...',
                'required':False,
            }),
            'book_edition':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Enter book\'s Edition...',
                'required':False,
            }),
            'number_in_stock':forms.NumberInput(attrs={
                'class':'form-control',
            }),
            'image':forms.ClearableFileInput(attrs={
                'class':'form-control', 'required':False,
            }),
            'book_pdf':forms.ClearableFileInput(attrs={
                'class':'form-control','required':False
            }),
            'pub_year':forms.DateInput(attrs={
                'class':'form-control','required':False,'type':'date'
            }),
            'pub_by':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Published By....',
                'required':False,
            }),
        }