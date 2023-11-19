from django.contrib import admin

# Register your models here.
from apps.rooms.models import RoomGroup, Room, RoomType

admin.site.register(RoomGroup)
admin.site.register(Room)
admin.site.register(RoomType)