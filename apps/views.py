#
# from django_filters.rest_framework import DjangoFilterBackend
# from drf_spectacular.utils import extend_schema
# from rest_framework.filters import OrderingFilter, SearchFilter
# from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView, \
#     RetrieveUpdateDestroyAPIView, ListCreateAPIView
#
# from apps.filters import UserFilterSet, OrderFilterSet, ProductFilterSet
# from apps.models import Category, Product, User, Order
# from apps.paginations import CustomPageNumberPagination
# from apps.serializers import CategoryModelSerializer, ProductModelSerializer, UserModelSerializer, OrderModelSerializer, \
#     RegisterModelSerializer
#
#
# #
# # class CategoryCreateAPIView(CreateAPIView):
# #     queryset = Category.objects.all()
# #     serializer_class = CategoryModelSerializer
# #
# # class CategoryDestroyAPIView(DestroyAPIView):
# #     queryset = Category.objects.all()
# #     serializer_class = CategoryModelSerializer
# #
# # class CategoryUpdateAPIView(UpdateAPIView):
# #     queryset = Category.objects.all()
# #     serializer_class = CategoryModelSerializer
# #
# # class CategoryRetrieveAPIView(RetrieveAPIView):
# #     queryset = Category.objects.all()
# #     serializer_class = CategoryModelSerializer
# class RegisterAPIView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterModelSerializer
#
# @extend_schema(tags=['categories'])
# class CategoryListCreateAPIView(ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryModelSerializer
#
# @extend_schema(tags=['categories'])
# class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryModelSerializer
#
# @extend_schema(tags=['products'])
# class ProductListCreateAPIView(ListCreateAPIView):
#     queryset =Product.objects.all()
#     serializer_class =ProductModelSerializer
#     filter_backends = DjangoFilterBackend, OrderingFilter, SearchFilter
#     # filterset_class = ProductFilterSet
#     pagination_class = None
#     search_fields = 'category__name',
#     ordering_fields = 'id',
#
# @extend_schema(tags=['products'])
# class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     queryset =Product.objects.all()
#     serializer_class =ProductModelSerializer
#
# @extend_schema(tags=['users'])
# class UserListAPIView(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserModelSerializer
#     filterset_class = UserFilterSet
#     pagination_class = CustomPageNumberPagination
#
# @extend_schema(tags=['orders'])
# class OrderListAPIView(ListAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderModelSerializer
#     filterset_class = OrderFilterSet