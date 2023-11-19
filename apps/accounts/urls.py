from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('account/', login_required(AccountList.as_view()), name='account'),
    path('account_create/', login_required(CreateAccount.as_view()), name='account_create'),
    path('account_update/<int:pk>/', login_required(UpdateAccount.as_view()), name='account_update'),
    path('get_open_account/', login_required(get_open_account), name='get_open_account'),
    path('open_account/', login_required(open_account), name='open_account'),
    path('get_close_account/', login_required(get_close_account), name='get_close_account'),
    path('close_account/', login_required(close_account), name='close_account'),
    path('validate_account/', login_required(validate_account), name='validate_account'),
    path('modal_payments/', login_required(modal_payments), name='modal_payments'),
    path('get_payments/', login_required(get_payments), name='get_payments'),
]