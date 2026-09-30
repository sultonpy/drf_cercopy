from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, TextField, IntegerField, ImageField, ForeignKey, CASCADE, TextChoices, DateTimeField

#
# class Category(Model):
#     name = CharField(max_length = 255)
#
# class Product(Model):
#     name = CharField(max_length = 255)
#     price = IntegerField(default=1_000)
#     category = ForeignKey('apps.Category', CASCADE, related_name='categories')
#     class Meta:
#         ordering = ['id']
#
# class ProductImage(Model):
#     product = ForeignKey('apps.Product', CASCADE, related_name='images')
#     image = ImageField(upload_to = 'products/%Y/%m/%d')
#
#
# class Order(Model):
#     class Status(TextChoices):
#         DELIVERING = 'delivering' , 'Delivering'
#         DELIVERED = 'delivered' , 'Delivered'
#         CANCELED = 'canceled' , 'Canceled'
#
#     owner = ForeignKey('apps.User', CASCADE, related_name='orders')
#     status =  CharField(max_length=25 ,choices = Status.choices, default = Status.DELIVERING)
#     created_at = DateTimeField(auto_now_add = True)
#

class User(AbstractUser):
    class Type(TextChoices):
        USER ='user' , 'User'
        ADMIN = 'admin', 'Admin'
        MANAGER = 'manager', 'Manager'

    phone = CharField(max_length = 255)
    balance = IntegerField(default=0)
    type = CharField(max_length=25 ,choices = Type.choices, default = Type.USER)
