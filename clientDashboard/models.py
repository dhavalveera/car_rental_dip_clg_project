from django.db import models
from django.conf import settings

# Create your models here.

class bookingDetails(models.Model):
    regUser = models.ForeignKey('account.regUsers', on_delete=models.CASCADE, related_name='bdregUsers')
    start_date = models.DateField()
    end_date = models.DateField()
    approxKMS = models.BigIntegerField()
    source = models.CharField(max_length=150)
    destination = models.CharField(max_length=150)
    driver_id = models.ForeignKey('driverDetails', on_delete=models.CASCADE, related_name='bddriverDetails')
    vehicles_id = models.ForeignKey('vehicles', on_delete=models.CASCADE, related_name='bdvechicles')


class bookingAccount(models.Model):
    bookingDetails_id = models.OneToOneField(bookingDetails, on_delete=models.CASCADE, related_name='babookingDetails')
    transactionType = models.CharField(max_length=150)
    transactionDate = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=150)


class vehicles(models.Model):
    brandName = models.CharField(max_length=150, null=False)
    modelName = models.CharField(max_length=150, null=False)
    rcNumber = models.CharField(max_length=150, null=False)
    perKmsCost = models.BigIntegerField()
    features = models.CharField(max_length=200)
    transmission = models.CharField(max_length=50, null=True)
    fuelType = models.CharField(max_length=50, null=True)
    minKMS = models.BigIntegerField()
    aftrKmPrice = models.BigIntegerField()
    seatingCapacity = models.CharField(max_length=50)
    carImg = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.brandName + ' ' + self.modelName


class driverDetails(models.Model):
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(max_length=254, unique=True)
    contactno = models.BigIntegerField()
    date_joined = models.DateTimeField(auto_now_add=True)
    licenseNumber = models.CharField(max_length=150)
    licenseExpiry = models.DateField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name