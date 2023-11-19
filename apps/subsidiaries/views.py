from datetime import datetime

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import SubsidiaryForm
from .models import Subsidiary
from ..products.models import Product
from ..users.models import User


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        user_id = self.request.user.id
        user_obj = User.objects.get(id=user_id)
        product = Product.objects.all()
        subsidiary = user_obj.subsidiary
        user = User.objects.all()
        date = datetime.now()
        if user_id is not None:
            context = {
                'users': user.count(),
                'products': product.count(),
                'date': date,
                'user_set': user
            }
            return context
        else:
            context = {
                # 'user_set': user_set,
            }
            return context


class ListSubsidiary(ListView):
    model = Subsidiary
    template_name = 'subsidiaries/subsidiary.html'
    context_object_name = 'subsidiary_set'
    queryset = Subsidiary.objects.all()


class CreateSubsidiary(CreateView):
    model = Subsidiary
    template_name = 'subsidiaries/subsidiary_form.html'
    form_class = SubsidiaryForm
    success_url = reverse_lazy('subsidiaries:subsidiary')


class UpdateSubsidiary(UpdateView):
    model = Subsidiary
    template_name = 'subsidiaries/subsidiary_form.html'
    form_class = SubsidiaryForm
    success_url = reverse_lazy('subsidiaries:subsidiary')


class DeleteSubsidiary(DeleteView):
    model = Subsidiary

    def post(self, request, pk, *args, **kwargs):
        subsidiary_obj = Subsidiary.objects.get(id=pk)
        subsidiary_obj.is_state = False
        subsidiary_obj.save()
        return redirect('subsidiaries:subsidiary')
