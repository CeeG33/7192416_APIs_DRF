from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from shop.models import Category, Product

class TestCategory(APITestCase):
    
    url = reverse_lazy("category-list")

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    def test_list(self):
        category = Category.objects.create(name="Fruits", active=True)
        Category.objects.create(name="Légumes", active=False)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        expected = [
            {
                "id": category.pk,
                "name": category.name,
                "date_created": self.format_datetime(category.date_created),
                "date_updated": self.format_datetime(category.date_updated)
            }
        ]
        self.assertEqual(expected, response.json())

    def test_create(self):
        self.assertFalse(Category.objects.exists())
        response = self.client.post(self.url, data={"name": "Tentative"})
        self.assertEqual(response.status_code, 405)
        self.assertFalse(Category.objects.exists())

    def test_detail(self):
        category = Category.objects.create(name="Fruits", active=True)
        Category.objects.create(name="Légumes", active=False)

        url_detail = reverse_lazy("category-detail", kwargs={"pk": category.pk})

        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, 200)

        expected = [
            {
                "id": category.pk,
                "name": category.name,
                "date_created": self.format_datetime(category.date_created),
                "date_updated": self.format_datetime(category.date_updated),
                "products": category.products,
            }
        ]
        self.assertEqual(expected, response.json())


class TestProduct(APITestCase):
    
    url = reverse_lazy("product-list")

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    def test_list(self):
        category = Category.objects.create(name="Fruits", active=True)
        product = Product.objects.create(name="Kiwi", active=True, category=category)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        expected = [
            {
                "id": product.pk,
                "name": product.name,
                "category": product.category_id,
                "date_created": self.format_datetime(product.date_created),
                "date_updated": self.format_datetime(product.date_updated),
            }
        ]

        self.assertEqual(expected, response.json())

    def test_create(self):
        self.assertFalse(Product.objects.exists())
        response = self.client.post(self.url, data={"name": "Tentative"})
        self.assertEqual(response.status_code, 405)
        self.assertFalse(Product.objects.exists())