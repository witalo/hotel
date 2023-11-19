from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('roomgroup/', login_required(ListRoomGroup.as_view()), name='roomgroup'),
    path('roomgroup_create/', login_required(CreateRoomGroup.as_view()), name='roomgroup_create'),
    path('roomgroup_update/<int:pk>/', login_required(UpdateRoomGroup.as_view()), name='roomgroup_update'),
    path('roomgroup_delete/<int:pk>/', login_required(DeleteRoomGroup.as_view()), name='roomgroup_delete'),
    path('get_rooms/', login_required(get_rooms), name='get_rooms'),
    path('get_rooms_grid/', login_required(get_rooms_grid), name='get_rooms_grid'),

    path('roomtype/', login_required(ListRoomType.as_view()), name='roomtype'),
    path('roomtype_create/', login_required(CreateRoomType.as_view()), name='roomtype_create'),
    path('roomtype_update/<int:pk>/', login_required(UpdateRoomType.as_view()), name='roomtype_update'),
    path('roomtype_delete/<int:pk>/', login_required(DeleteRoomType.as_view()), name='roomtype_delete'),

    path('room/', login_required(ListRoom.as_view()), name='room'),
    path('room_create/', login_required(CreateRoom.as_view()), name='room_create'),
    path('room_update/<int:pk>/', login_required(UpdateRoom.as_view()), name='room_update'),
    path('room_delete/<int:pk>/', login_required(DeleteRoom.as_view()), name='room_delete'),

    path('roomstate/', login_required(ListRoomState.as_view()), name='roomstate'),
    path('roomstate_create/', login_required(CreateRoomState.as_view()), name='roomstate_create'),
    path('roomstate_update/<int:pk>/', login_required(UpdateRoomState.as_view()), name='roomstate_update'),
    path('roomstate_delete/<int:pk>/', login_required(DeleteRoomState.as_view()), name='roomstate_delete'),
]
