# from datetime import timedelta
#
# from django.db.models import IntegerChoices
# from django.db.models.expressions import Exists, OuterRef
# from django.db.models.functions import Length
# from django.utils.timezone import now
# from django_filters import FilterSet, NumberFilter, BooleanFilter, ChoiceFilter
#
# #
# from apps.models import User, Order, Product, Category, ProductImage
#
#
# #
# #
# class UserFilterSet(FilterSet):
# #     min_price = NumberFilter(field_name="balance", lookup_expr='gte')
# #     max_price = NumberFilter(field_name="balance", lookup_expr='lte')
# #     is_owner = BooleanFilter(field_name='is_active', lookup_expr='exact')
# #     year = NumberFilter(method='last_login_year_filter')
# #
#     #
#     class Meta:
#         model = User
#         fields = []
# #
# #     def last_login_year_filter(self, qs, field_name, value):
# #         return qs.filter(last_login__year=value)
# class OrderFilterSet(FilterSet):
# #     class PeriodChoice(IntegerChoices):
# #         ONE_DAY = 1, '1 kun'
# #         THREE_DAY = 3, '3 kun'
# #         ONE_WEEK = 7, '1 hafta'
# #
# #     period = ChoiceFilter(choices=PeriodChoice.choices, method='period_filter')
# #
#     class Meta:
#         model = Order
#         fields = []
# #     def period_filter(self, qs, name, value):
# #         return qs.filter(created_at__gte=now() - timedelta(days=int(value)))
#
# class ProductFilterSet(FilterSet):
#     # class PeriodChoice(IntegerChoices):
#     #     ONE_DAY = 1, '1 kun'
#     #     THREE_DAY = 3, '3 kun'
#     #     ONE_WEEK = 7, '1 hafta'
#     #
#     # period = ChoiceFilter(choices=PeriodChoice.choices, method='period_filter')
#     # def period_filter(self, qs, name, value):
#     #     #     return qs.filter(created_at__gte=now() - timedelta(days=int(value)))
#
#     # c_later = NumberFilter(method='c_later_filter', label='How many later of Category name?')
#     has_image = BooleanFilter(method='filter_has_image')
#     class Meta:
#         model = Product
#         fields = []
#     #
#     # def c_later_filter(self, qs, name, value):
#     #     return qs.annotate(c_later=Length('category__name')).filter(c_later=value)
#     #
#
#
#     def filter_has_image(self, qs, name, value):
#         if value is True:
#             return qs.annotate(has_image=Exists(ProductImage.objects.filter(product_id=OuterRef('id')))).filter(has_image=True)
#         return qs
