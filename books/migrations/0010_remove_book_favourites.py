# Generated by Django 4.0.1 on 2022-01-23 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_alter_book_options_book_favourites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='favourites',
        ),
    ]
