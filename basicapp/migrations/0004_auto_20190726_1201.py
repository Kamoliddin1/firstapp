# Generated by Django 2.2 on 2019-07-26 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicapp', '0003_auto_20190725_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='choice',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]
