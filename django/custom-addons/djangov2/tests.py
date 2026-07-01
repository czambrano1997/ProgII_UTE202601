from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Categoria, Cliente, DetallePedido, Pedido, Producto


class ApiCrudTests(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Tecnología", descripcion="Equipos")
        self.producto = Producto.objects.create(
            categoria=self.categoria,
            nombre="Mouse",
            descripcion="Mouse inalámbrico",
            precio=Decimal("12.50"),
            stock=10,
        )
        self.cliente = Cliente.objects.create(
            cedula="1712345678",
            nombres="Ana",
            apellidos="Torres",
            email="ana@example.com",
            telefono="0999999999",
            direccion="Quito",
        )
        self.pedido = Pedido.objects.create(cliente=self.cliente, observacion="Entrega normal")
        self.detalle = DetallePedido.objects.create(
            pedido=self.pedido,
            producto=self.producto,
            cantidad=2,
            precio_unitario=Decimal("12.50"),
        )

    def test_categoria_crud(self):
        create_response = self.client.post(
            reverse("categoria-list"),
            {"nombre": "Accesorios", "descripcion": "Varios", "activo": True},
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        item_id = create_response.data["id"]
        detail_url = reverse("categoria-detail", args=[item_id])

        get_response = self.client.get(detail_url, format="json")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

        put_response = self.client.put(
            detail_url,
            {"nombre": "Accesorios PC", "descripcion": "Varios", "activo": True},
            format="json",
        )
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        patch_response = self.client.patch(detail_url, {"activo": False}, format="json")
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertFalse(patch_response.data["activo"])

        delete_response = self.client.delete(detail_url, format="json")
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_producto_crud(self):
        create_response = self.client.post(
            reverse("producto-list"),
            {
                "categoria": self.categoria.id,
                "nombre": "Teclado",
                "descripcion": "Teclado mecánico",
                "precio": "25.99",
                "stock": 5,
                "activo": True,
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        detail_url = reverse("producto-detail", args=[create_response.data["id"]])

        self.assertEqual(self.client.get(detail_url).status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.client.put(
                detail_url,
                {
                    "categoria": self.categoria.id,
                    "nombre": "Teclado USB",
                    "descripcion": "Teclado actualizado",
                    "precio": "27.50",
                    "stock": 7,
                    "activo": True,
                },
                format="json",
            ).status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(self.client.patch(detail_url, {"stock": 8}, format="json").status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.delete(detail_url).status_code, status.HTTP_204_NO_CONTENT)

    def test_cliente_crud(self):
        create_response = self.client.post(
            reverse("cliente-list"),
            {
                "cedula": "0912345678",
                "nombres": "Luis",
                "apellidos": "Pérez",
                "email": "luis@example.com",
                "telefono": "0988888888",
                "direccion": "Guayaquil",
                "activo": True,
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        detail_url = reverse("cliente-detail", args=[create_response.data["id"]])

        self.assertEqual(self.client.get(detail_url).status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.client.put(
                detail_url,
                {
                    "cedula": "0912345678",
                    "nombres": "Luis Alberto",
                    "apellidos": "Pérez",
                    "email": "luis@example.com",
                    "telefono": "0988888888",
                    "direccion": "Guayaquil",
                    "activo": True,
                },
                format="json",
            ).status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(self.client.patch(detail_url, {"direccion": "Cuenca"}, format="json").status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.delete(detail_url).status_code, status.HTTP_204_NO_CONTENT)

    def test_pedido_y_detalle_crud(self):
        pedido_response = self.client.post(
            reverse("pedido-list"),
            {"cliente": self.cliente.id, "estado": "PENDIENTE", "observacion": "Nuevo pedido", "activo": True},
            format="json",
        )
        self.assertEqual(pedido_response.status_code, status.HTTP_201_CREATED)
        pedido_id = pedido_response.data["id"]

        detalle_response = self.client.post(
            reverse("detalle-pedido-list"),
            {
                "pedido": pedido_id,
                "producto": self.producto.id,
                "cantidad": 1,
                "precio_unitario": "12.50",
            },
            format="json",
        )
        self.assertEqual(detalle_response.status_code, status.HTTP_201_CREATED)
        detalle_url = reverse("detalle-pedido-detail", args=[detalle_response.data["id"]])

        self.assertEqual(self.client.get(reverse("pedido-detail", args=[pedido_id])).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.patch(reverse("pedido-detail", args=[pedido_id]), {"estado": "PAGADO"}, format="json").status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.patch(detalle_url, {"cantidad": 2}, format="json").status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.delete(detalle_url).status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.client.delete(reverse("pedido-detail", args=[pedido_id])).status_code, status.HTTP_204_NO_CONTENT)

    def test_validaciones(self):
        producto_malo = self.client.post(
            reverse("producto-list"),
            {
                "categoria": self.categoria.id,
                "nombre": "Producto inválido",
                "precio": "0.00",
                "stock": 1,
            },
            format="json",
        )
        self.assertEqual(producto_malo.status_code, status.HTTP_400_BAD_REQUEST)

        cliente_malo = self.client.post(
            reverse("cliente-list"),
            {
                "cedula": "abc",
                "nombres": "Error",
                "apellidos": "Prueba",
                "email": "error@example.com",
            },
            format="json",
        )
        self.assertEqual(cliente_malo.status_code, status.HTTP_400_BAD_REQUEST)

        detalle_malo = self.client.post(
            reverse("detalle-pedido-list"),
            {
                "pedido": self.pedido.id,
                "producto": self.producto.id,
                "cantidad": 99,
                "precio_unitario": "12.50",
            },
            format="json",
        )
        self.assertEqual(detalle_malo.status_code, status.HTTP_400_BAD_REQUEST)
