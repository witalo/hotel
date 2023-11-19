from http import HTTPStatus
import json
import decimal
from django.core import serializers
from django.db.models import Max, Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from datetime import date, datetime

from apps.accounts.forms import AccountForm
from apps.accounts.models import Account, Payments
from apps.users.models import User


class AccountList(ListView):
    model = Account
    template_name = 'accounts/account.html'
    context_object_name = 'account_set'

    def get_context_data(self, **kwargs):
        account_set = Account.objects.all()
        context = {
            'account_set': account_set
        }
        return context


class CreateAccount(CreateView):
    model = Account
    template_name = 'accounts/account_form.html'
    form_class = AccountForm
    success_url = reverse_lazy('accounts:account')


class UpdateAccount(UpdateView):
    model = Account
    template_name = 'accounts/account_form.html'
    form_class = AccountForm
    success_url = reverse_lazy('accounts:account')


def validate_account(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        if pk:
            account_obj = Account.objects.get(id=int(pk))
            if account_obj.type == 'E':
                if account_obj.get_status() == 'C':
                    return JsonResponse({
                        'success': False,
                        'message': 'Aperture la caja',
                    }, status=HTTPStatus.OK)
                elif account_obj.get_status() == 'A':
                    return JsonResponse({
                        'success': True,
                        'message': 'Gracias',
                    }, status=HTTPStatus.OK)
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Aperture la caja',
                    }, status=HTTPStatus.OK)
            else:
                return JsonResponse({
                    'success': True,
                    'message': 'Gracias',
                }, status=HTTPStatus.OK)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Seleccione una caja o cuenta',
            }, status=HTTPStatus.OK)


def get_open_account(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        if pk:
            account_obj = Account.objects.get(id=int(pk))
            my_date = datetime.now()
            date_now = my_date.strftime("%Y-%m-%d")
            tpl = loader.get_template('accounts/account_open.html')
            context = ({
                'date_now': date_now,
                'account_obj': account_obj,
                'total': get_total(account_obj=account_obj)
            })
            return JsonResponse({
                'grid': tpl.render(context, request),
            }, status=HTTPStatus.OK, content_type="application/json")
        else:
            return JsonResponse({
                'success': False,
                'message': 'Problemas con la caja',
            }, status=HTTPStatus.OK)


def get_total(account_obj=None):
    total = []
    if account_obj.type == 'E':
        a_set = Payments.objects.filter(account=account_obj, payment='P', type='A', status='R')
        if a_set.exists():
            a_obj = a_set.last()
            total_aperture = a_obj.amount
            payment_set = Payments.objects.filter(account=account_obj, payment='P', status='R', number=a_obj.number)
            total_entry = payment_set.filter(type='I').aggregate(
                r=Coalesce(Sum('amount'), decimal.Decimal(0.00))).get('r')
            total_egress = payment_set.filter(type='E').aggregate(
                r=Coalesce(Sum('amount'), decimal.Decimal(0.00))).get('r')
        else:
            total_aperture = account_obj.initial
            total_entry = decimal.Decimal(0.00)
            total_egress = decimal.Decimal(0.00)
        subtotal = total_entry - total_egress
        total_cash = total_aperture + total_entry - total_egress
        c_total = {
            'total_aperture': round(total_aperture, 2),
            'total_entry': round(total_entry, 2),
            'total_egress': round(total_egress, 2),
            'total_account': round(subtotal, 2),
            'total': round(total_cash, 2)
        }
        total.append(c_total)
    elif account_obj.type == 'B':
        total_init = account_obj.initial
        payment_set = Payments.objects.filter(status='R', account=account_obj, payment='P')
        if payment_set:
            total_entry = payment_set.filter(type='I').aggregate(r=Coalesce(Sum('amount'), decimal.Decimal(0.00))).get(
                'r')
            total_egress = payment_set.filter(type='E').aggregate(r=Coalesce(Sum('amount'), decimal.Decimal(0.00))).get(
                'r')
        else:
            total_entry = decimal.Decimal(0.00)
            total_egress = decimal.Decimal(0.00)
        subtotal = total_entry - total_egress
        total_cash = total_init + total_entry - total_egress
        t_total = {
            'total_aperture': round(total_init, 2),
            'total_entry': round(total_entry, 2),
            'total_egress': round(total_egress, 2),
            'total_account': round(subtotal, 2),
            'total': round(total_cash, 2)
        }
        total.append(t_total)
    return total


@csrf_exempt
def open_account(request):
    if request.method == 'POST':
        pk = request.POST.get('account', '')
        date_now = request.POST.get('date-aperture', '')
        account_obj = Account.objects.get(id=int(pk))
        amount = decimal.Decimal(request.POST.get('amount-aperture', ''))
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        payment_obj = Payments(
            type='A',
            status='R',
            payment='P',
            description='APERTURA DE CAJA',
            amount=amount,
            user=user_obj,
            account=account_obj,
            date_payment=date_now,
            subsidiary=user_obj.subsidiary
        )
        payment_obj.save()
        payment_obj.number = payment_obj.id
        payment_obj.save()
        return JsonResponse({
            'success': True,
            'message': 'Apertura realizada',
        }, status=HTTPStatus.OK)


def get_close_account(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        if pk:
            account_obj = Account.objects.get(id=int(pk))
            dates = datetime.now()
            date_now = dates.strftime("%Y-%m-%d")
            tpl = loader.get_template('accounts/account_close.html')
            context = ({
                'date_now': date_now,
                'account_obj': account_obj,
                'total': get_total(account_obj=account_obj)
            })
            return JsonResponse({
                'success': True,
                'grid': tpl.render(context, request),
            }, status=HTTPStatus.OK, content_type="application/json")
        else:
            return JsonResponse({
                'success': False,
                'message': 'Problemas con la caja',
            }, status=HTTPStatus.OK)


@csrf_exempt
def close_account(request):
    if request.method == 'POST':
        pk = request.POST.get('id-account-close', '')
        date_now = request.POST.get('date-close', '')
        amount = (request.POST.get('total-account', ''))
        if amount:
            amount = decimal.Decimal(amount)
        else:
            amount = 0
        if pk:
            account_obj = Account.objects.get(id=int(pk))
        else:
            return JsonResponse({
                'success': False,
                'message': 'Caja no especificada',
            }, status=HTTPStatus.OK)
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        payment_obj = Payments(
            type='C',
            payment='P',
            status='R',
            description='CIERRE DE CAJA',
            amount=decimal.Decimal(amount),
            user=user_obj,
            account=account_obj,
            number=get_number_payment(account=account_obj),
            date_payment=date_now,
            subsidiary=user_obj.subsidiary
        )
        payment_obj.save()
        return JsonResponse({
            'success': True,
            'pk': payment_obj.id,
            'message': 'Caja cerrada con exito',
        }, status=HTTPStatus.OK)


def get_number_payment(account=None):
    if account is not None:
        if account.type == 'E':
            aperture_set = Payments.objects.filter(account=account, type='A')
            if aperture_set.exists():
                aperture_obj = aperture_set.last()
                n = aperture_obj.number
            else:
                return 0
        else:
            n = 0
        return int(n)
    else:
        return 0


def create_payment(order=None, pk=None, account=None, code='', user=None, amount=decimal.Decimal(0.00)):
    current = datetime.now()
    if order and account and user:
        if order.type == 'V' or order.type == 'S' or order.type == 'A':
            t = 'I'
        elif order.type == 'C' or order.type == 'E':
            t = 'E'
        payment_obj, created = Payments.objects.update_or_create(
            id=pk,
            defaults={
                "status": 'R',
                "type": t,
                "order": order,
                "payment": 'P',
                "description": 'PAGO REALIZADO',
                "code": code,
                "amount": amount,
                "date_payment": current.strftime("%Y-%m-%d"),
                "user": user,
                "subsidiary": user.subsidiary,
                "account": account,
                "number": get_number_payment(account=account)
            })


def modal_payments(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        if pk:
            account_obj = Account.objects.get(id=int(pk))
            my_date = datetime.now()
            date_now = my_date.strftime("%Y-%m-%d")
            tpl = loader.get_template('accounts/payments.html')
            context = ({
                'date': date_now,
                'account_obj': account_obj
            })
            return JsonResponse({
                'success': True,
                'grid': tpl.render(context, request),
            }, status=HTTPStatus.OK, content_type="application/json")
        else:
            return JsonResponse({
                'success': False,
                'message': 'Hubo algunos problemas',
            }, status=HTTPStatus.OK)


def get_payments(request):
    if request.method == 'GET':
        init = request.GET.get('init', '')
        end = request.GET.get('end', '')
        pk = request.GET.get('pk', '')
        if pk and init and end:
            try:
                account_obj = Account.objects.get(id=int(pk))
                payment_set = Payments.objects.filter(date_payment__range=(init, end),account=account_obj)
                t = loader.get_template('accounts/payments_grid.html')
                c = ({
                    'payment_set': payment_set
                })
                return JsonResponse({
                    'success': True,
                    'grid': t.render(c, request),
                })
            except Account.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'No se identifico la caja/cuenta',
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': str(e),
                })
