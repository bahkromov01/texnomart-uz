from django.contrib.auth.models import User
from django.db.models import Prefetch, Avg
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters import rest_framework as filters
from shop.models import AttributeKey, AttiributeValue, Product, Category, Image, Comment, ProductAttribute
from shop.serializers import ProductAttiributeKey, ProductAttiributeValue, ProductAttributeSerializer, \
    ProductSerializer, CategorySerializer, ProductDetailSerializer


class CategoryProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        queryset = Product.objects.filter(category__slug=category_slug).select_related('category')
        return queryset


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class ProductDetailView(RetrieveUpdateAPIView):
    serializer_class = ProductDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return Product.objects.prefetch_related(
            Prefetch('images', queryset=Image.objects.filter(is_primary=True)),
            Prefetch('comments', queryset=Comment.objects.select_related('user')),
            Prefetch('attributes', queryset=ProductAttribute.objects.all()),
            Prefetch(
                'user_likes',
                queryset=User.objects.filter(id=user.id),
                to_attr='user_likes'  # Ensure the attribute name is consistent
            )
        ).annotate(rating=Avg('comments__rating'))

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'id'
#
#     class ProductDetailView(RetrieveAPIView):
#         queryset = Product.objects.all()
#         serializer_class = ProductSerializer
#         lookup_field = 'id'
#
#         def get(self, request, *args, **kwargs):
#             product = self.get_object()
#
#             is_liked = product.is_liked(request.user)
#             comment_count = product.comments.count()
#             all_images = product.images.all()
#             attributes = product.attributes.all()
#             product_data = {
#                 'product_details': self.get_serializer(product).data,
#                 'is_liked': is_liked,
#                 'comment_count': comment_count,
#                 'all_images': [image.url for image in all_images],
#                 'attributes': [attr.name for attr in attributes]
#             }
#             return Response(product_data)
#
#         def update(self, request, *args, **kwargs):
#             product = self.get_object()
#             serializer = self.get_serializer(product, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             self.perform_update(serializer)
#             return Response(serializer.data)
#
#         def delete(self, request, *args, **kwargs):
#             product = self.get_object()
#             self.perform_destroy(product)
#             return Response(status=204)


class ProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        product_id = self.kwargs['product_id']
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        product_id = self.kwargs['product_id']
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        product_id = self.kwargs['product_id']
        product = Product.objects.get(id=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateProductView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


    # def get(self, request, *args, **kwargs):
    #     product_id = self.kwargs['product_id']
    #     product = get_object_or_404(Product, id=product_id)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # def put(self, request, *args, **kwargs):
    #     product_id = self.kwargs['product_id']
    #     product = get_object_or_404(Category, id=product_id)
    #     serializer = ProductSerializer(product, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        data = Product.objects.get(id=self.kwargs['id'])
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteProductView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Category, id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #
    def delete(self, request, *args, **kwargs):
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, slug=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductAttireKeyView(ListAPIView):
    queryset = AttributeKey.objects.all()
    serializer_class = ProductAttiributeKey

    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class ProductAttiributeValueView(ListAPIView):
    queryset = AttiributeValue.objects.all()
    serializer_class = ProductAttiributeValue

    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class ProductAttireView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAttributeSerializer
    lookup_field = 'id'

    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)




