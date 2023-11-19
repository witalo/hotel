import json
from datetime import datetime
from http import HTTPStatus
from django.contrib.auth.models import User, Group
from django.template import loader

from apps.users.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, JsonResponse
from .forms import FormLogin, UserForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.conf import settings
from django.core.mail import send_mail

from ..orders.models import Order
from ..products.models import Product


class Login(FormView):
    template_name = 'login.html'
    form_class = FormLogin
    success_url = reverse_lazy('home')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # return redirect(settings.LOGIN_REDIRECT_URL)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


class ListUser(ListView):
    model = User
    template_name = 'users/user.html'
    context_object_name = 'user_set'
    queryset = User.objects.filter(is_active=True)


class CreateUser(CreateView):
    model = User
    template_name = 'users/user_form.html'
    form_class = UserForm

    # success_url = reverse_lazy('users:user')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = User(
                username=form.cleaned_data.get('username'),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                document=form.cleaned_data.get('document'),
                email=form.cleaned_data.get('email'),
                phone=form.cleaned_data.get('phone'),
                subsidiary=form.cleaned_data.get('subsidiary')
            )
            new_user.set_password(form.cleaned_data.get('password_a'))
            new_user.save()
            return redirect('users:user')
        else:
            return render(request, self.template_name, {'form': form})


class UpdateUser(UpdateView):
    model = User
    template_name = 'users/user_form.html'
    form_class = UserForm

    def post(self, request, pk, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            user_obj = User.objects.get(id=int(pk))
            user_obj.username = form.cleaned_data.get('username')
            user_obj.first_name = form.cleaned_data.get('first_name')
            user_obj.last_name = form.cleaned_data.get('last_name')
            user_obj.document = form.cleaned_data.get('document')
            user_obj.email = form.cleaned_data.get('email')
            user_obj.phone = form.cleaned_data.get('phone')
            user_obj.subsidiary = form.cleaned_data.get('subsidiary')
            user_obj.set_password(form.cleaned_data.get('password_a'))
            user_obj.save()
            return redirect('users:user')
        else:
            return render(request, self.template_name, {'form': form})


class DeleteUser(DeleteView):
    model = User

    def post(self, request, pk, *args, **kwargs):
        user_obj = User.objects.get(id=pk)
        user_obj.is_active = False
        user_obj.save()
        return redirect('users:user')


def modal_user_permission(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        user_obj = User.objects.get(id=int(pk))
        group_set = Group.objects.all()
        group_user_set = []
        for g in group_set.order_by('id'):
            if user_obj.groups.filter(id=g.id).exists():
                val = True
            else:
                val = False
            l = {'pk': g.id, 'group_name': g.name, 'status': val}
            group_user_set.append(l)
        # user_group_set = User.groups.filter(name=group_obj.name).exists()
        t = loader.get_template('users/modal_permission_user.html')
        c = ({
            'group_user_set': group_user_set,
            'user_obj': user_obj
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_permission(request):
    if request.method == 'POST':
        pk = request.POST.get('pk', '')
        user = request.POST.get('user', '')
        user_obj = User.objects.get(id=int(user))
        state = bool(int(request.POST.get('state', 0)))
        group_obj = Group.objects.get(id=pk)
        if state:
            user_obj.groups.add(group_obj)
            return JsonResponse({'group': str(group_obj.name), 'message': 'Permiso agregado'}, status=HTTPStatus.OK)
        else:
            group_obj.user_set.remove(user_obj)
            return JsonResponse({'group': str(group_obj.name), 'message': 'Permiso removido'}, status=HTTPStatus.OK)
    else:
        return JsonResponse({'message': 'Error de peticion.'}, status=HTTPStatus.BAD_REQUEST)


@csrf_exempt
def create_permission(request):
    if request.method == 'POST':
        detail = request.POST.get('detail', '')
        row = json.loads(detail)
        user = row['user']
        user_obj = User.objects.get(id=int(user))
        for r in row['row']:
            state = bool(int(r['state']))
            pk = r['pk']
            group_obj = Group.objects.get(id=pk)
            if state:
                user_obj.groups.add(group_obj)
            else:
                group_obj.user_set.remove(user_obj)
        return JsonResponse({
            'success': True,
            'message': 'Operacion exitosa'
        }, status=HTTPStatus.OK)
    else:
        return JsonResponse({'success': False, 'message': 'Error de peticion.'}, status=HTTPStatus.BAD_REQUEST)
