# Generated by Django 2.2 on 2019-07-30 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicapp', '0005_auto_20190730_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='profile_image',
            field=models.ImageField(default='/media/default.jpg', upload_to='profile_pics'),
        ),
    ]