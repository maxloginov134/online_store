from django.shortcuts import render
from catalog.models import Product


def index(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list,
        'title': 'СберМаркетFast',
        'description': 'Как СберМаркет только быстрее, лучше и звонят сами когда заказ опаздывает на 3 дня.',
    }

    return render(request, 'catalog/home.html', context)


def contacts(request):
    context = {
        'title': 'Напишите нам!',
        'description': 'Мы постараемся вам ответить как можно скорее и решим любой ваш вопрос!',
    }

    return render(request, 'catalog/contacts.html', context)
