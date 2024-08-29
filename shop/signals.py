import os
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver
from confic.settings import BASE_DIR
from shop.models import Product, Category
import json

@receiver(pre_delete, sender=Product)
def save_product_before_delete(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'shop/delete/product', f'product_{instance.id}_backup.json')
    product_data = {
        'id': instance.id,
        'name': instance.name,
    }
    with open(file_path, 'w') as json_file:
        json.dump(product_data, json_file)


@receiver(pre_delete, sender=Category)
def save_category_before_delete(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'shop/delete/categories', f'category_{instance.id}_backup.json')
    category_data = {
        'id': instance.id,
        'name': instance.name,
        'slug': instance.slug
    }
    with open(file_path, 'w') as json_file:
        json.dump(category_data, json_file)
