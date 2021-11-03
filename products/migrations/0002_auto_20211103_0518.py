# Generated by Django 3.2.8 on 2021-11-03 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='thumbnail',
            new_name='thumbnail_image_url',
        ),
        migrations.RenameField(
            model_name='subcategory',
            old_name='main',
            new_name='main_category',
        ),
        migrations.AlterField(
            model_name='product',
            name='serial',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
