from http import HTTPStatus

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.rooms.forms import RoomGroupForm, RoomForm, RoomTypeForm, RoomStateForm
from apps.rooms.models import RoomGroup, Room, RoomType, RoomState


class ListRoomGroup(ListView):
    model = RoomGroup
    template_name = 'rooms/roomgroup.html'
    context_object_name = 'roomgroup_set'
    queryset = RoomGroup.objects.filter(is_state=True)


class CreateRoomGroup(CreateView):
    model = RoomGroup
    template_name = 'rooms/roomgroup_form.html'
    form_class = RoomGroupForm
    success_url = reverse_lazy('rooms:roomgroup')


class UpdateRoomGroup(UpdateView):
    model = RoomGroup
    template_name = 'rooms/roomgroup_form.html'
    form_class = RoomGroupForm
    success_url = reverse_lazy('rooms:roomgroup')


class DeleteRoomGroup(DeleteView):
    model = RoomGroup

    def post(self, request, pk, *args, **kwargs):
        roomgroup_obj = RoomGroup.objects.get(id=pk)
        roomgroup_obj.is_state = False
        roomgroup_obj.save()
        return redirect('rooms:roomgroup')


class ListRoom(ListView):
    model = Room
    template_name = 'rooms/room.html'
    context_object_name = 'room_set'
    queryset = Room.objects.filter(is_state=True)


class CreateRoom(CreateView):
    model = Room
    template_name = 'rooms/room_form.html'
    form_class = RoomForm
    success_url = reverse_lazy('rooms:room')


class UpdateRoom(UpdateView):
    model = Room
    template_name = 'rooms/room_form.html'
    form_class = RoomForm
    success_url = reverse_lazy('rooms:room')


class DeleteRoom(DeleteView):
    model = Room

    def post(self, request, pk, *args, **kwargs):
        room_obj = Room.objects.get(id=pk)
        room_obj.is_state = False
        room_obj.save()
        return redirect('rooms:room')


class ListRoomType(ListView):
    model = RoomType
    template_name = 'rooms/roomtype.html'
    context_object_name = 'roomtype_set'
    queryset = RoomType.objects.filter(is_state=True)


class CreateRoomType(CreateView):
    model = RoomType
    template_name = 'rooms/roomtype_form.html'
    form_class = RoomTypeForm
    success_url = reverse_lazy('rooms:roomtype')


class UpdateRoomType(UpdateView):
    model = RoomType
    template_name = 'rooms/roomtype_form.html'
    form_class = RoomTypeForm
    success_url = reverse_lazy('rooms:roomtype')


class DeleteRoomType(DeleteView):
    model = RoomType

    def post(self, request, pk, *args, **kwargs):
        roomtype_obj = RoomType.objects.get(id=pk)
        roomtype_obj.is_state = False
        roomtype_obj.save()
        return redirect('rooms:roomtype')


class ListRoomState(ListView):
    model = RoomState
    template_name = 'rooms/roomstate.html'
    context_object_name = 'roomstate_set'
    queryset = RoomState.objects.filter(is_state=True)


class CreateRoomState(CreateView):
    model = RoomState
    template_name = 'rooms/roomstate_form.html'
    form_class = RoomStateForm
    success_url = reverse_lazy('rooms:roomstate')


class UpdateRoomState(UpdateView):
    model = RoomState
    template_name = 'rooms/roomstate_form.html'
    form_class = RoomStateForm
    success_url = reverse_lazy('rooms:roomstate')


class DeleteRoomState(DeleteView):
    model = RoomState

    def post(self, request, pk, *args, **kwargs):
        roomstate_obj = RoomState.objects.get(id=pk)
        roomstate_obj.is_state = False
        roomstate_obj.save()
        return redirect('rooms:roomstate')


def get_rooms(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        if pk:
            try:
                group_obj = RoomGroup.objects.get(id=int(pk))
                room_set = Room.objects.filter(group=group_obj, is_state=True)
                room = []
                if room_set.exists():
                    for r in room_set.all():
                        f = {
                            'id': r.id,
                            'number': r.number,
                            'name': r.name,
                            't': r.type.id,
                            'type': r.type.name,
                            'state': r.state.color
                        }
                        room.append(f)
                    return JsonResponse({
                        'success': True,
                        'room': room
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Piso sin habitaciones',
                    })
            except RoomGroup.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'No existe el piso',
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': str(e),
                })


def get_rooms_grid(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        if pk:
            try:
                group_obj = RoomGroup.objects.get(id=int(pk))
                room_set = Room.objects.filter(group=group_obj, is_state=True)
                t = loader.get_template('orders/order_grid.html')
                c = ({
                    'room_set': room_set,
                    'type_set': RoomType.objects.filter(is_state=True)
                })
                return JsonResponse({
                    'success': True,
                    'grid': t.render(c, request),
                })
            except RoomGroup.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'No existe el piso',
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': str(e),
                })
