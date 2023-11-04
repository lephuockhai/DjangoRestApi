from django.db import models

# Create your models here.
class TokenInfomation(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    fullname = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=10)
    birth = models.DateField(null=True)
    avatar = models.BinaryField(null=True)
    role = models.CharField(max_length=20, choices=[('customer','Customer'), ('seller','Seller'), ('supplier','Supplier')], blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], null=True)
    
    class Meta:
        db_table = 'users'
    def __str__(self):
        return self.id