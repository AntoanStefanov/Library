# Generated by Django 4.0.1 on 2022-01-23 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_remove_book_favourites'),
        ('users', '0003_profile_favourites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='favourites',
            field=models.ManyToManyField(blank=True, default=None, related_name='favourites', to='books.Book'),
        ),
    ]
