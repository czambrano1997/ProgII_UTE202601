from django.test import TestCase
from rest_framework.test import APIClient

from inventario.models import Category, Supplier, Product, InventoryItem, Order


class InventoryApiCrudTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_category_crud(self):
        list_url = "/api/categories/"
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)

        create_response = self.client.post(
            list_url,
            {"name": "Bebidas", "description": "Productos lácteos"},
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)
        category_id = create_response.data["id"]

        detail_url = f"/api/categories/{category_id}/"
        self.assertEqual(self.client.get(detail_url).status_code, 200)
        self.assertEqual(self.client.put(detail_url, {"name": "Bebidas", "description": "Refrescos"}, format="json").status_code, 200)
        self.assertEqual(self.client.patch(detail_url, {"description": "Jugos y refrescos"}, format="json").status_code, 200)
        self.assertEqual(self.client.delete(detail_url).status_code, 204)

    def test_supplier_crud(self):
        list_url = "/api/suppliers/"
        create_response = self.client.post(
            list_url,
            {"name": "Proveedor Uno", "email": "proveedor@example.com", "phone": "123456", "address": "Montevideo", "active": True},
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)
        supplier_id = create_response.data["id"]

        detail_url = f"/api/suppliers/{supplier_id}/"
        self.assertEqual(self.client.get(detail_url).status_code, 200)
        self.assertEqual(self.client.put(detail_url, {"name": "Proveedor Uno", "email": "nuevo@example.com", "phone": "654321", "address": "Maldonado", "active": True}, format="json").status_code, 200)
        self.assertEqual(self.client.patch(detail_url, {"active": False}, format="json").status_code, 200)
        self.assertEqual(self.client.delete(detail_url).status_code, 204)

    def test_product_crud(self):
        category = Category.objects.create(name="Limpieza", description="Limpieza")
        supplier = Supplier.objects.create(name="Proveedor Dos", email="dos@example.com")
        list_url = "/api/products/"
        create_response = self.client.post(
            list_url,
            {"name": "Detergente", "sku": "DET-001", "description": "Detergente líquido", "price": "120.50", "category": category.id, "suppliers": [supplier.id], "active": True},
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)
        product_id = create_response.data["id"]

        detail_url = f"/api/products/{product_id}/"
        self.assertEqual(self.client.get(detail_url).status_code, 200)
        self.assertEqual(self.client.put(detail_url, {"name": "Detergente", "sku": "DET-001", "description": "Detergente premium", "price": "130.00", "category": category.id, "suppliers": [supplier.id], "active": True}, format="json").status_code, 200)
        self.assertEqual(self.client.patch(detail_url, {"price": "135.00"}, format="json").status_code, 200)
        self.assertEqual(self.client.delete(detail_url).status_code, 204)

    def test_inventory_item_crud(self):
        product = Product.objects.create(name="Arroz", sku="ARR-001", description="Arroz", price="100.00", category=None)
        list_url = "/api/inventory-items/"
        create_response = self.client.post(
            list_url,
            {"product": product.id, "quantity": 12, "location": "Bodega A"},
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)
        inventory_id = create_response.data["id"]

        detail_url = f"/api/inventory-items/{inventory_id}/"
        self.assertEqual(self.client.get(detail_url).status_code, 200)
        self.assertEqual(self.client.put(detail_url, {"product": product.id, "quantity": 15, "location": "Bodega B"}, format="json").status_code, 200)
        self.assertEqual(self.client.patch(detail_url, {"quantity": 20}, format="json").status_code, 200)
        self.assertEqual(self.client.delete(detail_url).status_code, 204)

    def test_order_crud(self):
        supplier = Supplier.objects.create(name="Proveedor Tres", email="tres@example.com")
        list_url = "/api/orders/"
        create_response = self.client.post(
            list_url,
            {"supplier": supplier.id, "date": "2026-07-02", "total": "250.00", "notes": "Pedido inicial"},
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)
        order_id = create_response.data["id"]

        detail_url = f"/api/orders/{order_id}/"
        self.assertEqual(self.client.get(detail_url).status_code, 200)
        self.assertEqual(self.client.put(detail_url, {"supplier": supplier.id, "date": "2026-07-03", "total": "260.00", "notes": "Actualizado"}, format="json").status_code, 200)
        self.assertEqual(self.client.patch(detail_url, {"notes": "Modificado"}, format="json").status_code, 200)
        self.assertEqual(self.client.delete(detail_url).status_code, 204)
