from django.urls import path, include
from django.contrib.auth.decorators import login_required
from apps.clients.views import ListClient, CreateClient, UpdateClient, DeleteClient, get_client_by_document, get_client, \
    client_save

urlpatterns = [
    path('client/', login_required(ListClient.as_view()), name='client'),
    path('client_create/', login_required(CreateClient.as_view()), name='client_create'),
    path('client_update/<int:pk>/', login_required(UpdateClient.as_view()), name='client_update'),
    path('client_delete/<int:pk>/', login_required(DeleteClient.as_view()), name='client_delete'),
    path('get_client_by_document/', login_required(get_client_by_document), name='get_client_by_document'),
    path('get_client/', login_required(get_client), name='get_client'),
    path('client_save/', login_required(client_save), name='client_save'),
]