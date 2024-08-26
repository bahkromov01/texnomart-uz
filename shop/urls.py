from django.urls import path
from shop.product.views import ProductListView, ProductAttireKeyView, ProductAttiributeValueView, ProductAttireView, \
    UpdateProductView, DeleteProductView
from shop.category.views import CategoryListView, CategoryDetail, CreateCategoryView, UpdateCategoryView, DeleteCategoryView
from shop.auth.views import LoginAPIView, RegisterAPIView, LogoutAPIView
from confic.custom_obtain_views import RegisterView, LoginView, LogoutView

urlpatterns = [
    # Category list
    path('categories/', CategoryListView.as_view()),
    path('category/<slug:category_slug>/detail', CategoryDetail.as_view()),
    path('category/add-category/', CreateCategoryView.as_view()),
    path('category/<slug:category_slug>/edit/', UpdateCategoryView.as_view()),
    path('category/<slug:category_slug>/delete/', DeleteCategoryView.as_view()),
    path('category/<slug:category_slug>/', ProductListView.as_view()),

    # Product list
    path('product/detail/<int:id>/', ProductListView.as_view()),
    # path('product/detail/<int:product_id>/', ProductDetailView.as_view()),
    path('product/<int:product_id>/edit/', UpdateProductView.as_view()),
    path('product/product_id /delete/', DeleteProductView.as_view()),

    # Attiribute
    path('attribute-key/', ProductAttireKeyView.as_view()),
    path('attribute-value/', ProductAttiributeValueView.as_view()),
    path('product-attiribute/', ProductAttireView.as_view()),

    # authentication
    path('login/', LoginAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),

    # JWT authentication
    path('register-page/', RegisterView.as_view(), name='register'),
    path('login-page/', LoginView.as_view(), name='login'),
    path('logout-page/', LogoutView.as_view(), name='logout'),


]
