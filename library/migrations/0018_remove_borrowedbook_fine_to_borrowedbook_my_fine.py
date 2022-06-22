# Generated by Django 4.0.4 on 2022-06-22 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0017_borrowedbook_date_to_return'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrowedbook',
            name='fine_to',
        ),
        migrations.AddField(
            model_name='borrowedbook',
            name='my_fine',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Fine Amount:'),
        ),
    ]
