from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('subsidiary/', login_required(ListSubsidiary.as_view()), name='subsidiary'),
    path('subsidiary_create/', login_required(CreateSubsidiary.as_view()), name='subsidiary_create'),
    path('subsidiary_update/<int:pk>/', login_required(UpdateSubsidiary.as_view()), name='subsidiary_update'),
    path('subsidiary_delete/<int:pk>/', login_required(DeleteSubsidiary.as_view()), name='subsidiary_delete'),
]