from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class UserInfomation(models.Model):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=150)
#     password = models.CharField(max_length=255)
#     email = models.CharField(max_length=255)
#     fullname = models.CharField(max_length=255, null=True)
#     address = models.CharField(max_length=255, null=True)
#     phone = models.CharField(max_length=10)
#     birth = models.DateField(null=True)
#     avatar = models.BinaryField(null=True)
#     role = models.CharField(max_length=20, choices=[('customer','Customer'), ('seller','Seller'), ('supplier','Supplier')], blank=True, null=True)
#     gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], null=True)
    
#     class Meta:
#         db_table = 'users'
#     def __str__(self):
#         return self.id
    
class CustomUser(AbstractUser):
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    gender = models.CharField(max_length = 10, null= True)

    class Meta:
        db_table = 'users'
    def __str__(self):
        return str(self.username)
    
class ProductInfomation(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=512, null=True)
    description = models.TextField(max_length=1000, null=True)
    cat_id = models.BigIntegerField(null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    stock = models.IntegerField(null=True)
    sold = models.IntegerField(null=True)
    shop_id = models.BigIntegerField(null=True)
    brand = models.CharField(max_length=255, null=True)
    price_min = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    image = models.URLField(max_length=500, null=True)
    images = models.JSONField(null= True)
    historical_sold = models.IntegerField(null=True)
    liked_count = models.IntegerField(null=True)
    class Meta:
        db_table = 'products'
    def __str__(self):
        return str(self.id)
    
class ReviewInfomation(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    user_id = models.BigIntegerField(null=True)
    product_id = models.BigIntegerField(null=True)
    score = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    comment = models.TextField(max_length=1000, null=True)
    comment_date = models.DateField(null=True)

    class Meta:
        db_table = 'reviews'
    def __str__(self):
        return str(self.id)
    
class ShippingRiceiveInfomation(models.Model):
    order_id = models.BigIntegerField(null=True)
    recipient_name = models.CharField(max_length=255, null=True)
    recipient_adress = models.CharField(max_length=255, null=True)
    recipient_phone = models.CharField(max_length=10, null=True)
    status = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'shipping_info'
    def __str__(self):
        return str(self.id)
    
class ShippingScheduleInfomation(models.Model):
    order_id = models.BigIntegerField(null=True)
    schedule_time = models.DateTimeField(null=True)
    schedule = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'shipping_schedule'
    def __str__(self):
        return str(self.order_id)
    
    
class ShopInfomation(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    user_id = models.BigIntegerField(null=True)
    logo = models.ImageField(upload_to='shop_logos/', null=True)

    class Meta:
        db_table = 'shops'
    def __str__(self):
        return str(self.id)

class CartInfomation(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    user_id = models.BigIntegerField(null=True)
    product_id = models.BigIntegerField(null=True)
    quantity = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    class Meta:
        db_table = 'shipping_carts'
    def __str__(self):
        return str(self.id)
    
class Orders(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    user_id = models.BigIntegerField(null=True)
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=20, null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    voucher_discount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    voucher_id = models.BigIntegerField(null=True)
    final_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    class Meta:
        db_table = 'orders'
    def __str__(self):
        return self.id
    
class OrderDetail(models.Model):
    order_id = models.BigIntegerField(null=True)
    product_id = models.BigIntegerField(null=True)
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    quantity = models.IntegerField(null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    class Meta:
        db_table = 'order_detail'
    def __str__(self):
        return self.order_id

class OrderPaymentInfomation(models.Model):
    order_id = models.BigIntegerField(null=True)
    create_at = models.DateField(null=True)
    method = models.CharField(max_length=64, null=True)
    status = models.CharField(max_length=20, null=True)
    final_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    class Meta:
        db_table = 'order_payment'
    def __str__(self):
        return str(self.order_id)

class VoucherInfomation(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    code = models.CharField(max_length=20, null=True)
    discount_type = models.CharField(max_length=10, null=True)
    discount_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    expiry_date = models.DateField(null=True)
    total_quantity = models.IntegerField(null=True)
    used_quantity = models.IntegerField(null=True)

    class Meta:
        db_table = 'vouchers'
    def __str__(self):
        return str(self.id)
    
class UserAddress(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    user_id = models.BigIntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=10, null=True)
    country = models.CharField(max_length=255, null=True)
    stage = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    district = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    default = models.BooleanField(default= False)

    class Meta:
        db_table = 'UserAddress'
    
    def __str__(self):
        return str(self.id)
    
