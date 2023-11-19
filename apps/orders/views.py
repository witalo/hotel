import decimal
import json
from datetime import datetime, timedelta
from http import HTTPStatus

from django.db.models import Max, Sum, F
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.template import loader
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from apps.accounts.models import Account, Payments
from apps.accounts.views import create_payment
from apps.clients.models import Client
from apps.orders.models import Order, OrderDetail
from apps.products.models import Product, ProductStore
from apps.products.views import store_output
from apps.rooms.models import RoomGroup, RoomType, Room, RoomState
from apps.users.models import User
from hotel import settings
from django.utils import timezone


class ListOrder(ListView):
    model = Order
    template_name = 'orders/order.html'
    context_object_name = 'order_set'

    def get_queryset(self):
        return RoomGroup.objects.filter(is_state=True)  # Consulta para obtener todos los productos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_set'] = RoomType.objects.filter(is_state=True)
        context['group_set'] = self.get_queryset()

        return context


def modal_orders(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        if pk:
            try:
                my_date = datetime.now()
                room_obj = Room.objects.get(id=int(pk))
                t = loader.get_template('orders/order_modal.html')
                c = ({
                    'room_obj': room_obj,
                    'order': room_obj.get_order(),
                    'date_now': my_date.strftime("%Y-%m-%dT%H:%M")
                })
                return JsonResponse({
                    'success': True,
                    'form': t.render(c, request),
                }, status=HTTPStatus.OK)
            except Room.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'No existe la habitacion',
                }, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': str(e),
                }, status=HTTPStatus.OK)


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        order_json = request.POST.get('order', '')
        order = json.loads(order_json)
        room_status = order['status']
        refund = order['refund']
        client = order['client']
        if int(client) > 0:
            client_obj = Client.objects.get(id=int(client))
        else:
            client_obj = None
        init = order['init']
        if init:
            init = timezone.make_aware(datetime.strptime(init, '%Y-%m-%dT%H:%M'), timezone.get_current_timezone())
        else:
            init = None
        end = order['end']
        if end:
            end = timezone.make_aware(datetime.strptime(end, '%Y-%m-%dT%H:%M'), timezone.get_current_timezone())
        else:
            end = None
        date_refund = order['date_refund']
        if date_refund:
            date_refund = timezone.make_aware(datetime.strptime(date_refund, '%Y-%m-%dT%H:%M'),
                                              timezone.get_current_timezone())
        else:
            date_refund = None
        price = order['price']
        room = order['room']
        room_obj = None
        if int(room) > 0:
            room_obj = Room.objects.get(id=int(room))
        else:
            room_obj = None
        user = request.user.id
        user_obj = User.objects.get(id=user)
        subsidiary_obj = user_obj.subsidiary
        current = datetime.now()
        order_status = 'P'
        if room_status == 'D':
            order_status = 'C'
        elif room_status == 'M':
            order_status = 'C'
        else:
            order_status = 'P'
        pk = order['order']
        if int(pk) > 0:
            pk = int(pk)
        else:
            pk = None
        obj, created = Order.objects.update_or_create(
            id=pk,
            defaults={
                "type": 'A',
                "number": get_correlative(subsidiary=subsidiary_obj, types='A', order=pk),
                "current": current.date(),
                "init": init,
                "end": end,
                "date_refund": date_refund,
                "price": decimal.Decimal(price),
                "refund": decimal.Decimal(refund),
                "user": user_obj,
                "client": client_obj,
                "subsidiary": subsidiary_obj,
                "status": order_status,
                "room": room_obj
            })
        if obj:
            for d in order['Detail']:
                detail = d['detail']
                product = d['product']
                product_obj = None
                if int(product) > 0:
                    product_obj = Product.objects.get(id=int(product))
                else:
                    product_obj = None
                description = d['description']
                quantity = d['quantity']
                if float(quantity) > 0:
                    quantity = decimal.Decimal(quantity)
                else:
                    quantity = decimal.Decimal(0.00)
                price = d['price']
                if float(price) > 0:
                    price = decimal.Decimal(price)
                else:
                    price = decimal.Decimal(0.00)
                store = d['store']
                store_obj = None
                if int(store) > 0:
                    store_obj = ProductStore.objects.get(id=int(store))
                else:
                    store_obj = None
                dk = None
                if int(detail) > 0:
                    dk = int(detail)
                else:
                    dk = None
                detail_obj, detail_created = OrderDetail.objects.update_or_create(
                    id=dk,
                    defaults={
                        "order": obj,
                        "product": product_obj,
                        "description": description,
                        "quantity": quantity,
                        "old_quantity": quantity,
                        "price": price,
                        "store": store_obj
                    })
                if detail_obj:
                    if detail_created and detail_obj.product:
                        store_output(detail=detail_obj)
            for p in order['Payment']:
                payment = p['payment']
                if int(payment) > 0:
                    payment = int(payment)
                else:
                    payment = None
                account = p['account']
                account_obj = None
                if int(account) > 0:
                    account_obj = Account.objects.get(id=int(account))
                else:
                    account_obj = None
                code = p['code']
                amount = p['amount']
                if float(amount) > 0:
                    amount = decimal.Decimal(amount)
                else:
                    amount = decimal.Decimal(0.00)
                create_payment(order=obj, pk=payment, account=account_obj, code=code, user=user_obj, amount=amount)
            room_state_obj = RoomState.objects.filter(type=room_status).first()
            room_obj.state = room_state_obj
            room_obj.save()
            return JsonResponse({
                'success': True,
                'order': obj.id,
                'status': room_status,
                'message': 'Operacion exitosa'
            }, status=HTTPStatus.OK)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Ocurrio un problema en el proceso'
            }, status=HTTPStatus.OK)
    else:
        return JsonResponse({'message': 'Error de peticion.'}, status=HTTPStatus.BAD_REQUEST)


def order_room(request, pk):
    if request.method == 'GET':
        my_date = datetime.now()
        room_obj = Room.objects.get(id=int(pk))
        product_set = Product.objects.filter(is_state=True)
        account_set = Account.objects.filter(is_state=True)
        return render(request, 'orders/order_room.html', {
            'product_set': product_set,
            'room_obj': room_obj,
            'account_set': account_set,
            'order': room_obj.get_order(),
            'state_set': RoomState._meta.get_field('type').choices,
            'date_now': my_date.strftime("%Y-%m-%dT%H:%M")
        })


def get_correlative(subsidiary=None, types=None, order=None):
    if order is not None:
        order_obj = Order.objects.get(id=int(order))
        return order_obj.number
    else:
        number = Order.objects.filter(type=types).aggregate(
            r=Coalesce(Max('number'), int(0))).get('r')
        return number + 1


class OrdersList(ListView):
    model = Account
    template_name = 'orders/orders.html'
    context_object_name = 'order_set'

    def get_context_data(self, **kwargs):
        my_date = datetime.now().date()
        order_set = Order.objects.filter(current__range=(my_date, my_date), type='A')
        context = {
            'order_set': order_set,
            'type_set': Order._meta.get_field('type').choices,
            'date': my_date.strftime("%Y-%m-%d")
        }
        return context


def get_orders(request):
    if request.method == 'GET':
        init = request.GET.get('init', '')
        end = request.GET.get('end', '')
        types = request.GET.get('type', '')
        if types and init and end:
            try:
                order_set = Order.objects.filter(current__range=(init, end), type=types)
                t = loader.get_template('orders/orders_grid.html')
                c = ({
                    'order_set': order_set
                })
                return JsonResponse({
                    'success': True,
                    'grid': t.render(c, request),
                })
            except Order.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'No existe ninguna orden',
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': str(e),
                })


def get_orders_month(request):
    if request.method == 'GET':
        date_ = datetime.now()
        year = date_.year
        month = date_.month
        user_id = request.user.id
        user_obj = User.objects.get(id=user_id)
        subsidiary_obj = user_obj.subsidiary
        sales = []
        purchase = []
        m = 1
        while m <= 12:
            s = OrderDetail.objects.filter(order__type__in=['V', 'A', 'S'],
                                           order__create_at__year=year, order__create_at__month=m,
                                           order__status='C', order__subsidiary=subsidiary_obj).aggregate(
                r=Coalesce(Sum(F('quantity') * F('price')), decimal.Decimal(0))).get('r')
            p = OrderDetail.objects.filter(order__type__in=['C', 'E'],
                                           order__create_at__year=year, order__create_at__month=m,
                                           order__status='C', order__subsidiary=subsidiary_obj).aggregate(
                r=Coalesce(Sum(F('quantity') * F('price')), decimal.Decimal(0))).get('r')
            sales.append(s)
            purchase.append(p)
            m += 1
        return JsonResponse({
            'sales': sales,
            'purchase': purchase,
        }, status=HTTPStatus.OK)


def get_room_week(request):
    if request.method == 'GET':
        date_ = datetime.now()
        week = date_.weekday()
        init = date_ - timedelta(days=int(week))
        user_id = request.user.id
        user_obj = User.objects.get(id=user_id)
        subsidiary_obj = user_obj.subsidiary
        output = []
        days = []
        for i in range(1, 8, 1):
            y = init.year
            m = init.month
            d = init.day
            room = Order.objects.filter(type='A', subsidiary=subsidiary_obj, create_at__year=y,
                                        create_at__month=m, create_at__day=d).aggregate(
                r=Coalesce(Sum('price'), decimal.Decimal(0.00))).get('r')
            refund = Order.objects.filter(type='A', subsidiary=subsidiary_obj, create_at__year=y,
                                          create_at__month=m, create_at__day=d).aggregate(
                r=Coalesce(Sum('refund'), decimal.Decimal(0.00))).get('r')
            output.append(room + refund)
            days.append(d)
            init = init + timedelta(days=1)
        return JsonResponse({
            'output': output,
            'days': days
        }, status=HTTPStatus.OK)
