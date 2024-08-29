# filters.py
import django_filters
from shop.models import Product, Category


class ProductFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['price', 'name', 'category']


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = ['title', 'slug']

