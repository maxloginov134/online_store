from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductList, contacts, PostList, PostCreate, DetailPost, PostUpdate, DeletePost

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductList.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('post_list/', PostList.as_view(), name='post_list'),
    path('post_form/', PostCreate.as_view(), name='post_form'),
    path('post_detail/<int:pk>/', DetailPost.as_view(), name='post_detail'),
    path('update_post/<int:pk>/', PostUpdate.as_view(), name='update_post'),
    path('post_delete/<int:pk>/', DeletePost.as_view(), name='post_delete'),
]
