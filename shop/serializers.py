
from django.contrib.auth.models import User
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from shop.models import Category, Product, Comment, ProductAttribute, AttributeKey, AttiributeValue


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    user_like = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField


    class Meta:
        model = Product
        fields = '__all__'

    def get_avg_rating(self, obj):
        if isinstance(obj, Product):
            avg_rating = obj.comments.aggregate(avg=Avg('rating'))['avg']
            if avg_rating is None:
                return 0
            return round(avg_rating, 2)
        else:
            return 0

    def get_user_like(self, products):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user_like = products.user_like.filter(id=request.user.id).exists()
            return user_like
        return False

    def get_image(self, obj):
        # image = Image.objects.filter(is_primary = True, product = obj).first()
        image = obj.images.filter(is_primary=True).first()
        if image:
            image_url = image.image.url
            request = self.context.get('request')
            return request.build_absolute_uri(image_url, 1000)


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['user'] = request.user
        return super().create(validated_data)


class ProductAttiributeKey(serializers.ModelSerializer):
    class Meta:
        model = AttributeKey
        fields = '__all__'




class ProductAttiributeValue(serializers.ModelSerializer):
    class Meta:
        model = AttiributeValue
        fields = '__all__'


class ProductAttributeSerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField()
    def get_attributes(self, products):
        attributes = ProductAttribute.objects.filter(product=products.id)
        attributes_dict = {}
        for attiribute in attributes:
            attributes_dict[attiribute.attiribute_key] = attiribute.attiribute_value
        return attributes_dict
    class Meta:
        model = Product
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name",
                  "last_name", "email", "password", "password2"]
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            detail = {
                "detail": "User Already exist!"
            }
            raise ValidationError(detail=detail)
        return username

    def validate(self, instance):
        if instance['password'] != instance['password2']:
            raise ValidationError({"message": "Both password must match"})

        if User.objects.filter(email=instance['email']).exists():
            raise ValidationError({"message": "Email already taken!"})

        return instance

    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        Token.objects.create(user=user)
        user.save()
        return user