from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True, blank=True, )
    discount = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    user_like = models.ManyToManyField(User)

    objects = models.Manager()

    @property
    def discount_price(self):
        if self.discount > 0:
            return self.price * (1 - (self.discount / 100))
        else:
            return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    is_primary = models.BooleanField(default=False)


class Comment(models.Model):
    class Rating(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5
    message = models.TextField()
    rating = models.IntegerField(choices=Rating.choices, default=Rating.one.value)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')


class AttributeKey(models.Model):
    key_name = models.CharField(max_length=125, null=True)

    def str(self):
        return self.key_name


class AttiributeValue(models.Model):
    value_name = models.CharField(max_length=125, null=True)

    def str(self):
        return self.value_name


class ProductAttribute(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    attiribute_key = models.ForeignKey('AttributeKey', on_delete=models.CASCADE)
    attiribute_value = models.ForeignKey('AttiributeValue', on_delete=models.CASCADE)
