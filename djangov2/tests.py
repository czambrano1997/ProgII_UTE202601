from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Product, Customer, Order, Review


class CategoryTestCase(TestCase):
    """Test suite for Category CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.category_data = {
            'name': 'Electronics',
            'description': 'Electronic devices and accessories'
        }

    def test_create_category(self):
        """Test POST: Create a new category"""
        response = self.client.post('/api/categories/', self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Electronics')

    def test_list_categories(self):
        """Test GET: List all categories"""
        Category.objects.create(**self.category_data)
        response = self.client.get('/api/categories/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_category(self):
        """Test GET: Retrieve a single category by ID"""
        category = Category.objects.create(**self.category_data)
        response = self.client.get(f'/api/categories/{category.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Electronics')

    def test_update_category(self):
        """Test PUT: Full update of a category"""
        category = Category.objects.create(**self.category_data)
        updated_data = {'name': 'Updated Electronics', 'description': 'Updated description'}
        response = self.client.put(f'/api/categories/{category.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Electronics')

    def test_partial_update_category(self):
        """Test PATCH: Partial update of a category"""
        category = Category.objects.create(**self.category_data)
        updated_data = {'name': 'Books'}
        response = self.client.patch(f'/api/categories/{category.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Books')

    def test_delete_category(self):
        """Test DELETE: Delete a category"""
        category = Category.objects.create(**self.category_data)
        response = self.client.delete(f'/api/categories/{category.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=category.id).exists())

    def test_invalid_category_name(self):
        """Test validation: Empty category name"""
        invalid_data = {'name': '', 'description': 'Test'}
        response = self.client.post('/api/categories/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductTestCase(TestCase):
    """Test suite for Product CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Electronics', description='Test')
        self.product_data = {
            'category': self.category.id,
            'name': 'Laptop',
            'description': 'High-performance laptop',
            'price': '999.99',
            'stock': 10
        }

    def test_create_product(self):
        """Test POST: Create a new product"""
        response = self.client.post('/api/products/', self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Laptop')
        self.assertEqual(float(response.data['price']), 999.99)

    def test_list_products(self):
        """Test GET: List all products"""
        Product.objects.create(**self.product_data)
        response = self.client.get('/api/products/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product(self):
        """Test GET: Retrieve a single product by ID"""
        product = Product.objects.create(**self.product_data)
        response = self.client.get(f'/api/products/{product.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Laptop')

    def test_update_product(self):
        """Test PUT: Full update of a product"""
        product = Product.objects.create(**self.product_data)
        updated_data = {
            'category': self.category.id,
            'name': 'Gaming Laptop',
            'description': 'High-end gaming laptop',
            'price': '1299.99',
            'stock': 5
        }
        response = self.client.put(f'/api/products/{product.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Gaming Laptop')

    def test_partial_update_product(self):
        """Test PATCH: Partial update of a product"""
        product = Product.objects.create(**self.product_data)
        updated_data = {'price': '1099.99'}
        response = self.client.patch(f'/api/products/{product.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['price']), 1099.99)

    def test_delete_product(self):
        """Test DELETE: Delete a product"""
        product = Product.objects.create(**self.product_data)
        response = self.client.delete(f'/api/products/{product.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_price(self):
        """Test validation: Negative price"""
        invalid_data = self.product_data.copy()
        invalid_data['price'] = '-10.00'
        response = self.client.post('/api/products/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_stock(self):
        """Test validation: Negative stock"""
        invalid_data = self.product_data.copy()
        invalid_data['stock'] = -5
        response = self.client.post('/api/products/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CustomerTestCase(TestCase):
    """Test suite for Customer CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.customer_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '1234567890'
        }

    def test_create_customer(self):
        """Test POST: Create a new customer"""
        response = self.client.post('/api/customers/', self.customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'John')

    def test_list_customers(self):
        """Test GET: List all customers"""
        Customer.objects.create(**self.customer_data)
        response = self.client.get('/api/customers/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_customer(self):
        """Test GET: Retrieve a single customer by ID"""
        customer = Customer.objects.create(**self.customer_data)
        response = self.client.get(f'/api/customers/{customer.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'john@example.com')

    def test_update_customer(self):
        """Test PUT: Full update of a customer"""
        customer = Customer.objects.create(**self.customer_data)
        updated_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'phone': '9876543210'
        }
        response = self.client.put(f'/api/customers/{customer.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Jane')

    def test_partial_update_customer(self):
        """Test PATCH: Partial update of a customer"""
        customer = Customer.objects.create(**self.customer_data)
        updated_data = {'phone': '5555555555'}
        response = self.client.patch(f'/api/customers/{customer.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '5555555555')

    def test_delete_customer(self):
        """Test DELETE: Delete a customer"""
        customer = Customer.objects.create(**self.customer_data)
        response = self.client.delete(f'/api/customers/{customer.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_email(self):
        """Test validation: Invalid email format"""
        invalid_data = self.customer_data.copy()
        invalid_data['email'] = 'invalid-email'
        response = self.client.post('/api/customers/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email(self):
        """Test validation: Duplicate email"""
        Customer.objects.create(**self.customer_data)
        response = self.client.post('/api/customers/', self.customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderTestCase(TestCase):
    """Test suite for Order CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
        self.order_data = {
            'customer': self.customer.id,
            'items': [{'product_id': 1, 'quantity': 2, 'price': '50.00'}],
            'total': '100.00',
            'status': 'pending'
        }

    def test_create_order(self):
        """Test POST: Create a new order"""
        response = self.client.post('/api/orders/', self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'pending')

    def test_list_orders(self):
        """Test GET: List all orders"""
        Order.objects.create(**self.order_data)
        response = self.client.get('/api/orders/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_order(self):
        """Test GET: Retrieve a single order by ID"""
        order = Order.objects.create(**self.order_data)
        response = self.client.get(f'/api/orders/{order.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'pending')

    def test_update_order_status(self):
        """Test PUT: Update order status"""
        order = Order.objects.create(**self.order_data)
        updated_data = {
            'customer': self.customer.id,
            'items': order.items,
            'total': order.total,
            'status': 'paid'
        }
        response = self.client.put(f'/api/orders/{order.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'paid')

    def test_partial_update_order(self):
        """Test PATCH: Partial update of order"""
        order = Order.objects.create(**self.order_data)
        updated_data = {'status': 'shipped'}
        response = self.client.patch(f'/api/orders/{order.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'shipped')

    def test_delete_order(self):
        """Test DELETE: Delete an order"""
        order = Order.objects.create(**self.order_data)
        response = self.client.delete(f'/api/orders/{order.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_total(self):
        """Test validation: Negative total"""
        invalid_data = self.order_data.copy()
        invalid_data['total'] = '-100.00'
        response = self.client.post('/api/orders/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_status(self):
        """Test validation: Invalid status"""
        invalid_data = self.order_data.copy()
        invalid_data['status'] = 'invalid_status'
        response = self.client.post('/api/orders/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReviewTestCase(TestCase):
    """Test suite for Review CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            category=self.category,
            name='Laptop',
            price='999.99',
            stock=10
        )
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
        self.review_data = {
            'product': self.product.id,
            'customer': self.customer.id,
            'rating': 5,
            'comment': 'Excellent product!'
        }

    def test_create_review(self):
        """Test POST: Create a new review"""
        response = self.client.post('/api/reviews/', self.review_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 5)

    def test_list_reviews(self):
        """Test GET: List all reviews"""
        Review.objects.create(**self.review_data)
        response = self.client.get('/api/reviews/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_review(self):
        """Test GET: Retrieve a single review by ID"""
        review = Review.objects.create(**self.review_data)
        response = self.client.get(f'/api/reviews/{review.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 5)

    def test_update_review(self):
        """Test PUT: Full update of a review"""
        review = Review.objects.create(**self.review_data)
        updated_data = {
            'product': self.product.id,
            'customer': self.customer.id,
            'rating': 4,
            'comment': 'Very good product.'
        }
        response = self.client.put(f'/api/reviews/{review.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 4)

    def test_partial_update_review(self):
        """Test PATCH: Partial update of a review"""
        review = Review.objects.create(**self.review_data)
        updated_data = {'rating': 3}
        response = self.client.patch(f'/api/reviews/{review.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 3)

    def test_delete_review(self):
        """Test DELETE: Delete a review"""
        review = Review.objects.create(**self.review_data)
        response = self.client.delete(f'/api/reviews/{review.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_rating_too_high(self):
        """Test validation: Rating above 5"""
        invalid_data = self.review_data.copy()
        invalid_data['rating'] = 10
        response = self.client.post('/api/reviews/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_rating_too_low(self):
        """Test validation: Rating below 1"""
        invalid_data = self.review_data.copy()
        invalid_data['rating'] = 0
        response = self.client.post('/api/reviews/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
