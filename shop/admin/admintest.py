import unittest
from flask import url_for
from flask_testing import TestCase
from shop import app, db, bcrypt
from shop.admin.models import User
from shop.products.models import Brand, Category, Addproduct
from shop.customer.models import CustomerOrder

class FlaskTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        return app

    def setUp(self):
        db.create_all()
        # Create a test user
        hashed_pw = bcrypt.generate_password_hash('password')
        test_user = User(name='Test User', username='testuser', email='test@example.com', password=hashed_pw)
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, email, password):
        return self.client.post(
            url_for('login'),
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def test_admin_route(self):
        # Test accessing admin route without login
        response = self.client.get(url_for('admin'))
        self.assertIn(b'login first please', response.data)

        # Test accessing admin route after login
        self.login('test@example.com', 'password')
        response = self.client.get(url_for('admin'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Page', response.data)

    def test_registration(self):
        response = self.client.post(
            url_for('register'),
            data=dict(name='New User', username='newuser', email='new@example.com', password='password'),
            follow_redirects=True
        )
        self.assertIn(b'Thank you for Registering', response.data)

    def test_login_logout(self):
        response = self.login('test@example.com', 'password')
        self.assertIn(b'you are logedin now', response.data)

        response = self.client.get(url_for('logout'), follow_redirects=True)
        self.assertIn(b'You have been logged out successfully', response.data)

    def test_brands_route(self):
        self.login('test@example.com', 'password')
        response = self.client.get(url_for('brands'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Brands', response.data)

    def test_category_route(self):
        self.login('test@example.com', 'password')
        response = self.client.get(url_for('category'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Category', response.data)

    def test_orders_route(self):
        self.login('test@example.com', 'password')
        response = self.client.get(url_for('admin_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Orders', response.data)

if __name__ == '__main__':
    unittest.main()
