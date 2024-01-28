from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

from .views_pdf import ticket, ticket_refund

urlpatterns = [
    path('order/', login_required(ListOrder.as_view()), name='order'),
    path('modal_orders/', login_required(modal_orders), name='modal_orders'),
    path('create_order/', login_required(create_order), name='create_order'),
    path('order_room/<int:pk>/', login_required(order_room), name='order_room'),
    path('ticket/<int:pk>/', login_required(ticket), name='ticket'),
    path('ticket_refund/<int:pk>/', login_required(ticket_refund), name='ticket_refund'),
    path('orders/', login_required(OrdersList.as_view()), name='orders'),
    path('get_orders/', login_required(get_orders), name='get_orders'),
    path('get_orders_month/', login_required(get_orders_month), name='get_orders_month'),
    path('get_room_week/', login_required(get_room_week), name='get_room_week'),

    path('purchase/', login_required(ListPurchase.as_view()), name='purchase'),
    path('create_purchase/', login_required(create_purchase), name='create_purchase'),
]
