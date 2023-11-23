from http import HTTPStatus

import decimal
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.products.forms import ProductBrandForm, ProductForm
from apps.products.models import Product, ProductBrand, ProductStore
from apps.subsidiaries.models import Subsidiary
from apps.users.models import User
from hotel import settings


class ListProduct(ListView):
    model = Product
    template_name = 'products/product.html'  # Define la plantilla HTML
    context_object_name = 'products'  # Nombre del objeto en el contexto

    def get_queryset(self):
        return Product.objects.filter(is_state=True)  # Consulta para obtener todos los productos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.get_queryset()
        page = self.request.GET.get('page')  # Obtiene el número de página de la solicitud
        paginator = Paginator(products, settings.PAGINATION_PER_PAGE)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # Si el número de página no es un entero, muestra la primera página
            products = paginator.page(1)
        except EmptyPage:
            # Si el número de página está fuera de rango, muestra la última página
            products = paginator.page(paginator.num_pages)

        context['products'] = products
        return context


class CreateProduct(CreateView):
    model = Product
    template_name = 'products/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('products:product')


class UpdateProduct(UpdateView):
    model = Product
    template_name = 'products/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('products:product')

    # def form_valid(self, form):
    #     # Guarda el formulario pero no lo guarda en la base de datos todavía
    #     producto = form.save(commit=False)
    #
    #     # Obtiene la imagen del formulario
    #     imagen = self.request.FILES.get('image')
    #
    #     # Guarda la imagen en la carpeta 'products' dentro de la carpeta de medios
    #     producto.image = imagen
    #     producto.save()
    #
    #     return super().form_valid(form)


class DeleteProduct(DeleteView):
    model = Product

    def post(self, request, pk, *args, **kwargs):
        product_obj = Product.objects.get(id=pk)
        product_obj.is_state = False
        product_obj.save()
        return redirect('products:product')


def search_product(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        user = request.user.id
        user_obj = User.objects.get(id=int(user))
        product = []
        if search:
            product_set = Product.objects.filter(name__icontains=search)
            for p in product_set:
                product.append({
                    'pk': p.id,
                    'name': p.name.upper(),
                    'code': p.code.upper(),
                    'brand': p.product_brand.name,
                    'price': p.price,
                    'stock': p.get_store(user_obj)
                })
        return JsonResponse({
            'status': True,
            'product': product
        })


def get_product_by_id(request):
    if request.method == 'GET':
        pk = request.GET.get('pk')
        user = request.user.id
        user_obj = User.objects.get(id=int(user))
        if pk:
            product_obj = Product.objects.get(id=int(pk))
            return JsonResponse({
                'success': True,
                'code': product_obj.code,
                'name': product_obj.name,
                'price': product_obj.price,
                'store': product_obj.get_store(user_obj),
            }, status=HTTPStatus.OK)
        else:
            return JsonResponse({
                'success': False,
                'code': 'No se logro obtener el producto'
            }, status=HTTPStatus.OK)


class ListProductBrand(ListView):
    model = ProductBrand
    template_name = 'products/brand.html'
    context_object_name = 'brand_set'
    queryset = ProductBrand.objects.all()


class CreateProductBrand(CreateView):
    model = ProductBrand
    template_name = 'products/brand_form.html'
    form_class = ProductBrandForm
    success_url = reverse_lazy('products:brand')


class UpdateProductBrand(UpdateView):
    model = ProductBrand
    template_name = 'products/brand_form.html'
    form_class = ProductBrandForm
    success_url = reverse_lazy('products:brand')


class DeleteProductBrand(DeleteView):
    model = ProductBrand

    def post(self, request, pk, *args, **kwargs):
        brand_obj = ProductBrand.objects.get(id=pk)
        brand_obj.is_state = False
        brand_obj.save()
        return redirect('products:brand')


def modal_inventory(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        if pk:
            try:
                product_obj = Product.objects.get(id=int(pk))
                t = loader.get_template('products/inventory.html')
                c = ({
                    'product_obj': product_obj,
                    'inventory': get_inventory(product_obj)
                })
                return JsonResponse({
                    'success': True,
                    'form': t.render(c, request),
                }, status=HTTPStatus.OK)
            except Product.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'No existe el producto',
                }, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': str(e),
                }, status=HTTPStatus.OK)


def get_inventory(product):
    inventory = []
    for s in Subsidiary.objects.filter(is_state=True).all().order_by('id'):
        store_set = ProductStore.objects.filter(product=product, subsidiary=s)
        stock = decimal.Decimal(0.00)
        if store_set.exists():
            store_obj = store_set.first()
            stock = decimal.Decimal(store_obj.quantity)
            val = True
        else:
            stock = decimal.Decimal(0.00)
            val = False
        a = {
            'id': s.id,
            'serial': s.serial,
            'name': s.name,
            'stock': stock,
            'val': val
        }
        inventory.append(a)
    return inventory


@csrf_exempt
def create_inventory(request):
    if request.method == 'POST':
        s = request.POST.get('subsidiary', '')
        p = request.POST.get('product', '')
        q = request.POST.get('quantity', '')
        product_obj = Product.objects.get(id=int(p))
        subsidiary_obj = Subsidiary.objects.get(id=int(s))
        if product_obj and subsidiary_obj:
            store_obj = ProductStore(
                quantity=decimal.Decimal(q),
                product=product_obj,
                subsidiary=subsidiary_obj
            )
            store_obj.save()
            if store_obj:
                return JsonResponse({
                    'success': True,
                    'message': 'Inventario creado'
                }, status=HTTPStatus.OK)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Producto sin identificar'
            }, status=HTTPStatus.OK)


def store_input(detail=None):
    if detail is not None:
        store_obj = detail.store
        old_stock = store_obj.quantity
        new_stock = old_stock + detail.quantity
        store_obj.quantity = new_stock
        store_obj.save()


def store_output(detail=None):
    if detail is not None:
        store_obj = detail.store
        old_stock = store_obj.quantity
        new_stock = old_stock - detail.quantity
        store_obj.quantity = new_stock
        store_obj.save()
