from http import HTTPStatus

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.clients.api import ApisNetPe
from apps.clients.forms import ClientForm
from apps.clients.models import Client

APIS_TOKEN = "apis-token-1693.sJwdqJzDvppWBtjEtTuupNuH4GMgWpfc"
api_net = ApisNetPe(APIS_TOKEN)


# Create your views here.

class ListClient(ListView):
    model = Client
    template_name = 'clients/client.html'
    context_object_name = 'client_set'
    queryset = Client.objects.filter(is_state=True)


class CreateClient(CreateView):
    model = Client
    template_name = 'clients/client_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('clients:client')


class UpdateClient(UpdateView):
    model = Client
    template_name = 'clients/client_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('clients:client')


class DeleteClient(DeleteView):
    model = Client

    def post(self, request, pk, *args, **kwargs):
        client_obj = Client.objects.get(id=pk)
        client_obj.is_state = False
        client_obj.save()
        return redirect('clients:client')


def get_client_by_document(request):
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


def get_client(request):
    if request.method == 'GET':
        document = request.GET.get('document', '')
        try:
            client_obj = Client.objects.get(document=document)
        except Client.DoesNotExist:
            client_obj = None
        if client_obj is not None:
            return JsonResponse({
                'pk': client_obj.id,
                'names': client_obj.names,
                'phone': client_obj.phone,
                'address': client_obj.address},
                status=HTTPStatus.OK)
        else:
            if len(document) == 8:
                r = api_net.get_person(document)
                if r.get('success') is True:
                    name = r.get('nombres')
                    first_name = r.get('paterno')
                    last_name = r.get('materno')
                    address = r.get('direccion')
                    if name is not None and len(first_name) > 0:
                        names = "{} {} {}".format(name, first_name, last_name)
                        client_obj = Client(
                            document=document,
                            names=names,
                            address=address
                        )
                        client_obj.save()
                        return JsonResponse({
                            'pk': client_obj.id,
                            'names': client_obj.names,
                            'phone': client_obj.phone,
                            'address': client_obj.address,
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
            elif len(document) == 11:
                r = api_net.get_company(document)
                if r.get('success') is True:
                    names = r.get('razon_social')
                    address = r.get('direccion_completa')
                    if names is not None and len(names) > 0:
                        client_obj = Client(
                            document=document,
                            names=names,
                            address=address
                        )
                        client_obj.save()
                        return JsonResponse({
                            'pk': client_obj.id,
                            'names': client_obj.names,
                            'phone': client_obj.phone,
                            'address': client_obj.address},
                            status=HTTPStatus.OK)
                    else:
                        data = {
                            'error': 'No se encontro registro del ruc en la sunat, registre manualmente'}
                        response = JsonResponse(data)
                        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                        return response
                else:
                    return JsonResponse({
                        'pk': 0,
                        'message': 'No se encontro registro del ruc en la sunat, registre manualmente'},
                        status=HTTPStatus.OK)

    else:
        return JsonResponse({'error': 'Error de petición.'}, status=HTTPStatus.BAD_REQUEST)


@csrf_exempt
def client_save(request):
    if request.method == 'POST':
        pk = request.POST.get('pk', '')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        if pk:
            client_obj = Client.objects.get(id=int(pk))
            client_obj.address = address
            client_obj.phone = phone
            client_obj.save()
            return JsonResponse({
                'success': True,
                'pk': client_obj.id,
                'message': 'Proceso con exito',
            }, status=HTTPStatus.OK)
        else:
            return JsonResponse({
                'success': False,
                'message': 'seleccione una persona',
            }, status=HTTPStatus.OK)
