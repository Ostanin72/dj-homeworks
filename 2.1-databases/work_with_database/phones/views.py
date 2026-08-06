from django.shortcuts import render, redirect, get_object_or_404

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    phone_list = Phone.objects.all()
    sort_param = request.GET.get('sort', '')
    if sort_param == 'name':
        phone_list = phone_list.order_by('name')
    elif sort_param == 'min_price':
        phone_list = phone_list.order_by('price')
    elif sort_param == 'max_price':
        phone_list = phone_list.order_by('-price')

    context = {
        'phones': phone_list
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone_product = get_object_or_404(Phone, slug=slug)

    context = {
        'phone': phone_product
    }

    return render(request, template, context)
