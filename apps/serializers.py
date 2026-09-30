# from django.contrib.auth.hashers import make_password
# from rest_framework.exceptions import ValidationError
# from rest_framework.fields import CharField
# from rest_framework.serializers import ModelSerializer
#
# from apps.models import Category, Product, User, Order
#
#
# class RegisterModelSerializer(ModelSerializer):
#     password = CharField(max_length=255,write_only=True)
#     confirm_password = CharField(max_length=255,write_only=True)
#     class Meta:
#         model = User
#         fields = ['username', 'phone', 'password', 'confirm_password']
#
#     def validate_username(self, value : str):
#         if not value.isalpha():
#             raise ValidationError('Username must be alphanumeric')
#         return value
#
#     def validate_phone(self, value ):
#         if not value.startswith('+') or len(value) != 13:
#             raise ValidationError('Phone number must be 13 digits')
#         return value
#
#     def validate(self, data):
#         password = data.get('password')
#         confirm_password = data.pop('confirm_password', None)
#         if password != confirm_password:
#             raise ValidationError('Passwords must match')
#         data['password'] = make_password(password)
#         return data
#
#
# class CategoryModelSerializer(ModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'
#
#     def validate_name(self, value):
#         if value.startwith('vali'):
#             raise ValidationError('Vali deb boshlanmasin!')
#         return value
#
#
#
# class ProductModelSerializer(ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'
#
# class UserModelSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = 'id', 'first_name', 'last_name','username','phone'
#
# class OrderModelSerializer(ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'
