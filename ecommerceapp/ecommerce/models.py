from re import Pattern
from xmlrpc.client import DateTime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CASCADE
from ckeditor.fields import RichTextField

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrator'
    SELLER = 'SELLER', 'Seller'
    CUSTOMER = 'CUSTOMER', 'Customer'

class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    avatar = models.ImageField(upload_to='profile/%Y/%m')
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER
    )

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    store_name = models.CharField(max_length=255)
    store_description = models.TextField(blank=True)

    def __str__(self):
        return self.store_name

class Category(BaseModel):
    category_name = models.CharField(max_length=255, null=False, unique=True)
    description= models.TextField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name

class Product(BaseModel):
    product_name = models.CharField(max_length=50, null=False)
    description = models.TextField(max_length=255, null=False)
    price = models.FloatField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.PositiveIntegerField(default=0)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    categories = models.ManyToManyField(Category, related_name='products', blank=True)

    def __str__(self):
        return self.product_name

class Cart(models.Model):
    date_add = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Cart Items'

class Payment(models.Model):
    orders = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='payments', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField()
    method = models.CharField(
        max_length=20,
        choices=[
            ('COD', 'Cash on Delivery'),
            ('PAYPAL', 'PayPal'),
            ('STRIPE', 'Stripe'),
            ('ZALOPAY', 'ZaloPay'),
            ('MOMO', 'MoMo')
        ]
    )


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    total_price = models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_details')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    total_price = models.FloatField()
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Order Details'

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    review = RichTextField(blank=True)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)



# Create your models here.
