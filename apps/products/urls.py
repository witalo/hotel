from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('product/', login_required(ListProduct.as_view()), name='product'),
    path('product_create/', login_required(CreateProduct.as_view()), name='product_create'),
    path('product_update/<int:pk>/', login_required(UpdateProduct.as_view()), name='product_update'),
    path('product_delete/<int:pk>/', login_required(DeleteProduct.as_view()), name='product_delete'),

    path('brand/', login_required(ListProductBrand.as_view()), name='brand'),
    path('brand_create/', login_required(CreateProductBrand.as_view()), name='brand_create'),
    path('brand_update/<int:pk>/', login_required(UpdateProductBrand.as_view()), name='brand_update'),
    path('brand_delete/<int:pk>/', login_required(DeleteProductBrand.as_view()), name='brand_delete'),
    path('search_product/', login_required(search_product), name='search_product'),
    path('modal_inventory/', login_required(modal_inventory), name='modal_inventory'),
    path('create_inventory/', login_required(create_inventory), name='create_inventory'),
    path('get_product_by_id/', login_required(get_product_by_id), name='get_product_by_id'),
]
