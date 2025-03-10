import unittest
from flask import url_for
from flask_testing import TestCase
from shop import app, db, bcrypt
from shop.admin.models import User
from shop.products.models import Addproduct, Brand, Category
from shop.customer.models import CustomerOrder

class FlaskTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SECRET_KEY'] = 'testsecret'
        return app

    def setUp(self):
        # Create tables
        db.create_all()

        # Create a test user
        hashed_pw = bcrypt.generate_password_hash('password').decode('utf-8')
        test_user = User(name='Test User', username='testuser', email='test@example.com', password=hashed_pw)
        db.session.add(test_user)
        db.session.commit()

        # Create a test brand, category, and product
        test_category = Category(name='Test Category')
        test_brand = Brand(name='Test Brand')
        db.session.add(test_category)
        db.session.add(test_brand)
        db.session.commit()

        test_product = Addproduct(name='Test Product', price=100, description='Test Description', brand_id=1, category_id=1)
        db.session.add(test_product)
        db.session.commit()

        # Create a test order
        test_order = CustomerOrder(product_id=1, customer_id=1, quantity=2)
        db.session.add(test_order)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Helper method to login
    def login(self, email, password):
        return self.client.post(
            url_for('login'),
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def test_admin_route_without_login(self):
        response = self.client.get(url_for('admin'))
        self.assertRedirects(response, url_for('login'))  # Expecting a redirect to login page
        self.assertIn(b'login first please', response.data)

    def test_admin_route_with_login(self):
        self.login('test@example.com', 'password')  # Login as the test user
        response = self.client.get(url_for('admin'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Page', response.data)  # Verify 'Admin Page' is in the response

    def test_brands_route_without_login(self):
        response = self.client.get(url_for('brands'))
        self.assertRedirects(response, url_for('login'))  # Expecting a redirect to login page
        self.assertIn(b'you should be login to contenu', response.data)

    def test_brands_route_with_login(self):
        self.login('test@example.com', 'password')
        response = self.client.get(url_for('brands'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Brand', response.data)  # Verify the brand name appears

    def test_category_route_without_login(self):
        response = self.client.get(url_for('category'))
        self.assertRedirects(response, url_for('login'))  # Expecting a redirect to login page
        self.assertIn(b'your should be logiin to continue', response.data)

    def test_category_route_with_login(self):
        self.login('test@example.com', 'password')
        response = self.client.get(url_for('category'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Category', response.data)  # Verify the category name appears

    def test_register_route(self):
        response = self.client.get(url_for('register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register page', response.data)  # Verify the registration page is rendered

    def test_login_route_with_valid_credentials(self):
        response = self.login('test@example.com', 'password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'you are logedin now', response.data)  # Verify the login success message

    def test_login_route_with_invalid_credentials(self):
        response = self.client.post(
            url_for('login'),
            data=dict(email='test@example.com', password='wrongpassword'),
            follow_redirects=True
        )
        self.assertIn(b'Wrong email and password', response.data)  # Verify error message for wrong login

    def test_logout_route(self):
        self.login('test@example.com', 'password')
        response = self.client.get(url_for('logout'), follow_redirects=True)
        self.assertIn(b'You have been logged out successfully!', response.data)  # Verify logout success message

    def test_admin_orders_route_without_login(self):
        response = self.client.get(url_for('admin_orders'))
        self.assertRedirects(response, url_for('login'))  # Expecting a redirect to login page
        self.assertIn(b'Please log in first!', response.data)

    def test_admin_orders_route_with_login(self):
        self.login('test@example.com', 'password')
        response = self.client.get(url_for('admin_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Orders', response.data)  # Verify 'All Orders' is in the response

    def test_view_order_route(self):
        self.login('test@example.com', 'password')
        response = self.client.get(url_for('view_order', order_id=1))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Product', response.data)  # Verify product in the order details

if __name__ == '__main__':
    unittest.main()
