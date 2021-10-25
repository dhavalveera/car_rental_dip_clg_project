# Generated by Django 3.1.6 on 2021-02-12 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='driverDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contactno', models.BigIntegerField()),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('licenseNumber', models.CharField(max_length=150)),
                ('licenseExpiry', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='vehicles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brandName', models.CharField(max_length=150)),
                ('modelName', models.CharField(max_length=150)),
                ('rcNumber', models.CharField(max_length=150)),
                ('perKmsCost', models.BigIntegerField()),
                ('features', models.CharField(max_length=200)),
                ('minKMS', models.BigIntegerField()),
                ('aftrKmPrice', models.BigIntegerField()),
                ('seatingCapacity', models.CharField(max_length=50)),
                ('carImg', models.FileField(upload_to='images/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='bookingDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('approxKMS', models.BigIntegerField()),
                ('source', models.CharField(max_length=150)),
                ('destination', models.CharField(max_length=150)),
                ('driver_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bddriverDetails', to='clientDashboard.driverdetails')),
                ('regUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bdregUsers', to='account.regusers')),
                ('vehicles_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bdvechicles', to='clientDashboard.vehicles')),
            ],
        ),
        migrations.CreateModel(
            name='bookingAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transactionType', models.CharField(max_length=150)),
                ('transactionDate', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('description', models.CharField(max_length=150)),
                ('bookingDetails_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='babookingDetails', to='clientDashboard.bookingdetails')),
            ],
        ),
    ]
