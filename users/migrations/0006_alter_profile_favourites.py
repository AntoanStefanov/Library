# Generated by Django 4.0.1 on 2022-01-27 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_remove_book_favourites'),
        ('users', '0005_alter_profile_favourites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='favourites',
            field=models.ManyToManyField(to='books.Book'),
        ),
    ]
