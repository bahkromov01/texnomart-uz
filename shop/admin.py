from django.contrib import admin

from shop.models import Category, Product, Image, Comment, AttributeKey, AttiributeValue, ProductAttribute


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


@admin.register(Image)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('rating',)


@admin.register(AttributeKey)
class AttributeKeyAdmin(admin.ModelAdmin):
    list_display = ('key_name',)


@admin.register(AttiributeValue)
class AttiributeValueAdmin(admin.ModelAdmin):
    list_display = ('value_name',)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ()