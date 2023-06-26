from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductList, contacts, PostList, PostCreate, DetailPost, PostUpdate, DeletePost, \
    ProductCreate, UpdateProduct, DetailProduct, DeleteProduct

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductList.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),

    path('product_create/', ProductCreate.as_view(), name='product_create'),
    path('update_product/<int:pk>/', UpdateProduct.as_view(), name='update_product'),
    path('detail_product/<int:pk>/', DetailProduct.as_view(), name='product_detail'),
    path('product_delete/<int:pk>/', DeleteProduct.as_view(), name='product_delete'),

    path('post_list/', PostList.as_view(), name='post_list'),
    path('post_form/', PostCreate.as_view(), name='post_form'),
    path('post_detail/<int:pk>/', DetailPost.as_view(), name='post_detail'),
    path('update_post/<int:pk>/', PostUpdate.as_view(), name='update_post'),
    path('post_delete/<int:pk>/', DeletePost.as_view(), name='post_delete'),
]
