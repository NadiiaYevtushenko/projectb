import requests
from .models import ConcreteProduct


def sync_products_from_project_a():
    response = requests.get('http://127.0.0.1:8000/api/products/')
    if response.status_code == 200:
        products = response.json()
        for product_data in products:
            ConcreteProduct.objects.update_or_create(
                title=product_data['title'],
                defaults={
                    'description': product_data['description'],
                    'price': product_data['price'],
                }
            )
