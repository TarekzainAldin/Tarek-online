import unittest
from shop import app, db, bcrypt
from shop.admin.models import User
from shop.products.models import Brand, Category, Addproduct
from shop.customer.models import CustomerOrder
import json  # Import json

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config.update({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SECRET_KEY': 'test-key',
            'WTF_CSRF_ENABLED': False
        })
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, email, password):
        return self.client.post('/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)

    def test_admin_access_with_login(self):
        with app.app_context():
            hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')
            user = User(
                name='Admin User',
                username='adminuser',
                email='admin@test.com',
                password=hashed_pw
            )
            db.session.add(user)
            db.session.commit()

        response = self.login('admin@test.com', 'password123')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/admin', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Page', response.data)

    def test_login_logout(self):
        with app.app_context():
            hashed_pw = bcrypt.generate_password_hash('testpass').decode('utf-8')
            user = User(
                name='Test User',
                username='testuser',
                email='test@test.com',
                password=hashed_pw
            )
            db.session.add(user)
            db.session.commit()

        response = self.login('test@test.com', 'testpass')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'welcome test@test.com you are logedin now', response.data)

        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out successfully!', response.data)



    def test_brands_page(self):
        with app.app_context():
            hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')
            admin = User(name='Admin', username='admin', email='admin@test.com', password=hashed_pw)
            db.session.add(admin)
            brand = Brand(name='Test Brand')
            db.session.add(brand)
            db.session.commit()

        self.login('admin@test.com', 'password123')
        response = self.client.get('/brands', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Brands', response.data)
        self.assertIn(b'Test Brand', response.data)

    def test_categories_page(self):
        with app.app_context():
            hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')
            admin = User(name='Admin', username='admin', email='admin@test.com', password=hashed_pw)
            db.session.add(admin)
            category = Category(name='Test Category')
            db.session.add(category)
            db.session.commit()

        self.login('admin@test.com', 'password123')
        response = self.client.get('/category', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Category', response.data)
        self.assertIn(b'Test Category', response.data)

    def test_admin_orders_page(self):
        with app.app_context():
            hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')
            admin = User(name='Admin', username='admin', email='admin@test.com', password=hashed_pw)
            db.session.add(admin)
            customer = User(name='Customer', email='cust@test.com', username='cust', password='pw')
            db.session.add(customer)
            db.session.commit()

            order = CustomerOrder(
                invoice='12345',
                status='Pending',
                customer_id=customer.id,
                orders='[]'  # Make sure this is a valid JSON string
            )
            db.session.add(order)
            db.session.commit()

        self.login('admin@test.com', 'password123')
        response = self.client.get('/admin/orders', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Orders', response.data)

if __name__ == '__main__':
    unittest.main()
