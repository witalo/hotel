from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('user/', login_required(ListUser.as_view()), name='user'),
    path('user_create/', login_required(CreateUser.as_view()), name='user_create'),
    path('user_update/<int:pk>/', login_required(UpdateUser.as_view()), name='user_update'),
    path('user_delete/<int:pk>/', login_required(DeleteUser.as_view()), name='user_delete'),
    path('modal_user_permission/', login_required(modal_user_permission), name='modal_user_permission'),
    path('save_permission/', login_required(save_permission), name='save_permission'),
    path('create_permission/', login_required(create_permission), name='create_permission'),
]