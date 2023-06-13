from django.core.management import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        fruits = Category.objects.get(title='Фрукты')
        vegetables = Category.objects.get(title='Овощи')

        products_list = [
            {'title': 'Апельсин', 'description': 'Фрукт',
             'image': 'images/orange.jpg', 'category': fruits, 'price': 49.95},
            {'title': 'Перец красный сладкий', 'description': 'Овощ',
             'image': 'images/pepper.jpg', 'category': vegetables, 'price': 68.7}
        ]

        Product.objects.all().delete()

        products_for_create = []

        for product in products_list:
            products_for_create.append(
                Product(**product)
            )

        Product.objects.bulk_create(products_for_create)
