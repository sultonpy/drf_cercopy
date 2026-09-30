# from django.urls import path
#
# from apps.views import CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView, ProductListCreateAPIView, \
#     ProductRetrieveUpdateDestroyAPIView, UserListAPIView, OrderListAPIView, RegisterAPIView
#
# # CategoryDestroyAPIView, CategoryUpdateAPIView, CategoryRetrieveAPIView, CategoryCreateAPIView
# urlpatterns = [
#     # path('categories', CategoryCreateAPIView.as_view()),
#     # path('categories/<int:pk>', CategoryDestroyAPIView.as_view()),
#     # path('categories/<int:pk>', CategoryUpdateAPIView.as_view()),
#     # path('categories/<int:pk>', CategoryRetrieveAPIView.as_view()),
#     path('categories', CategoryListCreateAPIView.as_view()),
#     path('categories/<int:pk>', CategoryRetrieveUpdateDestroyAPIView.as_view()),
#     path('products', ProductListCreateAPIView.as_view()),
#     path('users', UserListAPIView.as_view()),
#     path('orders', OrderListAPIView.as_view()),
#     path('products/<int:pk>', ProductRetrieveUpdateDestroyAPIView.as_view()),
#     path('users/register', RegisterAPIView.as_view()),
#
# ]
