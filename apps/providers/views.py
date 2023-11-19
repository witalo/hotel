from http import HTTPStatus

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.clients.api import ApisNetPe
from apps.providers.forms import ProviderForm
from apps.providers.models import Provider

APIS_TOKEN = "apis-token-1693.sJwdqJzDvppWBtjEtTuupNuH4GMgWpfc"
api_net = ApisNetPe(APIS_TOKEN)


# Create your views here.

class ListProvider(ListView):
    model = Provider
    template_name = 'providers/provider.html'
    context_object_name = 'provider_set'
    queryset = Provider.objects.filter(is_state=True)


class CreateProvider(CreateView):
    model = Provider
    template_name = 'providers/provider_form.html'
    form_class = ProviderForm
    success_url = reverse_lazy('providers:provider')


class UpdateProvider(UpdateView):
    model = Provider
    template_name = 'providers/provider_form.html'
    form_class = ProviderForm
    success_url = reverse_lazy('providers:client')


class DeleteProvider(DeleteView):
    model = Provider

    def post(self, request, pk, *args, **kwargs):
        client_obj = Provider.objects.get(id=pk)
        client_obj.is_state = False
        client_obj.save()
        return redirect('providers:provider')


def get_provider_by_document(request):
    if request.method == 'GET':
        document = request.GET.get('document', '')
        r = api_net.get_person(document)
        if r.get('success') is True:
            name = r.get('nombres')
            first_name = r.get('paterno')
            last_name = r.get('materno')
            address = r.get('direccion')
            if name is not None and len(first_name) > 0:
                names = "{} {} {}".format(name, first_name, last_name)
            return JsonResponse({
                'names': names,
                'address': address},
                status=HTTPStatus.OK)
        else:
            data = {
                'error': 'No se encontro registro del dni en la reniec, registre manualmente'}
            response = JsonResponse(data)
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return response
    else:
        return JsonResponse({'error': 'Error de petición.'}, status=HTTPStatus.BAD_REQUEST)


def get_provider(request):
    if request.method == 'GET':
        document = request.GET.get('document', '')
        try:
            provider_obj = Provider.objects.get(document=document)
        except Provider.DoesNotExist:
            provider_obj = None
        if provider_obj is not None:
            return JsonResponse({
                'pk': provider_obj.id,
                'names': provider_obj.names,
                'phone': provider_obj.phone,
                'address': provider_obj.address,
                'message': 'Operacion exitosa'},
                status=HTTPStatus.OK)
        else:
            r = api_net.get_person(document)
            if r.get('success') is True:
                name = r.get('nombres')
                first_name = r.get('paterno')
                last_name = r.get('materno')
                address = r.get('direccion')
                if name is not None and len(first_name) > 0:
                    names = "{} {} {}".format(name, first_name, last_name)
                    provider_obj = Provider(
                        document=document,
                        names=names,
                        address=address
                    )
                    provider_obj.save()
                    return JsonResponse({
                        'pk': provider_obj.id,
                        'names': provider_obj.names,
                        'phone': provider_obj.phone,
                        'address': provider_obj.address,
                        'message': 'Operacion exitosa'},
                        status=HTTPStatus.OK)
                else:
                    data = {
                        'error': 'No se encontro registro del dni en la reniec, registre manualmente'}
                    response = JsonResponse(data)
                    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                    return response
            else:
                return JsonResponse({
                    'pk': 0,
                    'message': 'No se encontro registro del dni en la reniec, registre manualmente'},
                    status=HTTPStatus.OK)
    else:
        return JsonResponse({'error': 'Error de petición.'}, status=HTTPStatus.BAD_REQUEST)


@csrf_exempt
def provider_save(request):
    if request.method == 'POST':
        pk = request.POST.get('pk', '')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        if pk:
            provider_obj = Provider.objects.get(id=int(pk))
            provider_obj.address = address
            provider_obj.phone = phone
            provider_obj.save()
            return JsonResponse({
                'success': True,
                'pk': provider_obj.id,
                'message': 'Proceso con exito',
            }, status=HTTPStatus.OK)
        else:
            return JsonResponse({
                'success': False,
                'message': 'seleccione una persona',
            }, status=HTTPStatus.OK)
