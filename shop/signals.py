import os

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver

from confic import settings
from confic.settings import BASE_DIR, DEFAULT_FROM_EMAIL
from shop.models import Product, Category
import json



@receiver(post_save, sender=Product)
def saved_product(sender, instance, **kwargs):
    subject = 'Product has been created'
    message = (f"Product \"{instance.name}\" has been created\nCheck this out: http://51.21.11.250:8000/"
               f" \n\nCreated Time: {instance.created_at}\n\n\nAdmin Name: admin\nAdmin Password: 123")
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = ['jasurmavlonov24@gmail.com', 'baxromovruslan322@gmail.com']

    send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Category)
def saved_product(sender, instance, **kwargs):
    subject = 'Category has been created'
    message = (f"Category \"{instance.title}\" has been created\nCheck this out: http://51.21.11.250:8000/"
               f" \n\nCreated Time: {instance.created_at}\n\n\nAdmin Name: admin\nAdmin Password: 123")
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = ['jasurmavlonov24@gmail.com', 'baxromovruslan322@gmail.com']

    send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=Product)
@receiver(post_delete, sender=Product)
def save_product_before_delete(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'shop/delete/product', f'product_{instance.id}_backup.json')
    product_data = {
        'id': instance.id,
        'name': instance.name,
        'slug': instance.slug,
        'description': instance.description,
        'discount': instance.discount,

    }
    with open(file_path, 'w') as json_file:
        json.dump(product_data, json_file)


@receiver(pre_delete, sender=Category)
@receiver(post_delete, sender=Category)
def save_category_before_delete(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'shop/delete/categories', f'category_{instance.id}_backup.json')
    category_data = {
        'id': instance.id,
        'name': instance.name,
        'slug': instance.slug
    }
    with open(file_path, 'w') as json_file:
        json.dump(category_data, json_file)


# @receiver(post_save, sender=Product)
# @receiver(post_save, sender=Category)
# def send_notification_email(sender, instance, created, **kwargs):
#     if created:
#         if sender == Product:
#             subject = 'The product has been created'
#             message = f'The product has been created: {instance.name}'
#         elif sender == Category:
#             subject = 'The category has been created'
#             message = f'The category has been created: {instance.title}'
#
#     recipient_list = User.objects.values_list('email', flat=True)
#
#     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
#
#
# @receiver(post_delete, sender=Product)
# @receiver(post_delete, sender=Category)
# def send_notification_on_delete(sender, instance, **kwargs):
#     if sender == Product:
#         subject = 'The product has been deleted'
#         message = f'The product has been deleted: {instance.name}'
#     elif sender == Category:
#         subject = 'The category has been deleted'
#         message = f'The category has been deleted: {instance.title}'
#
#     recipient_list = User.objects.values_list('email', flat=True)
#     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)