# Generated by Django 3.1.6 on 2021-02-26 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientDashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicles',
            name='carImg',
            field=models.FileField(blank=True, upload_to='cars/'),
        ),
    ]
