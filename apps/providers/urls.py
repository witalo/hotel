from django.urls import path, include
from django.contrib.auth.decorators import login_required
from apps.providers.views import ListProvider, CreateProvider, UpdateProvider, DeleteProvider, get_provider_by_document, \
    get_provider, provider_save

urlpatterns = [
    path('provider/', login_required(ListProvider.as_view()), name='provider'),
    path('provider_create/', login_required(CreateProvider.as_view()), name='provider_create'),
    path('provider_update/<int:pk>/', login_required(UpdateProvider.as_view()), name='provider_update'),
    path('provider_delete/<int:pk>/', login_required(DeleteProvider.as_view()), name='provider_delete'),
    path('get_provider_by_document/', login_required(get_provider_by_document), name='get_provider_by_document'),
    path('get_provider/', login_required(get_provider), name='get_provider'),

    path('provider_save/', login_required(provider_save), name='provider_save'),
]
