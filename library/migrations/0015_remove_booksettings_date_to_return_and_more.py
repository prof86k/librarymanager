# Generated by Django 4.0.4 on 2022-06-22 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_borrowedbook_confirm_returned_book_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booksettings',
            name='date_to_return',
        ),
        migrations.AddField(
            model_name='booksettings',
            name='number_of_day_to_return',
            field=models.PositiveIntegerField(null=True, verbose_name='Days to Return Book:'),
        ),
    ]