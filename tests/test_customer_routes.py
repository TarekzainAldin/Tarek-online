import pytest
from flask import url_for
from shop import app, db
from shop.customer.models import Register, CustomerOrder

# Fixture to set up the Flask test client and database
@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

# Test for customer registration
def test_customer_register(client):
    response = client.post('/customer/register', data={
        'name': 'Test User',
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'country': 'Testland',
        'city': 'Testville',
        'contact': '1234567890',
        'address': '123 Test St',
        'zipcode': '12345'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Thank you for registering' in response.data

# Test for customer login
def test_customer_login(client):
    # Register a user first
    client.post('/customer/register', data={
        'name': 'Test User',
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'country': 'Testland',
        'city': 'Testville',
        'contact': '1234567890',
        'address': '123 Test St',
        'zipcode': '12345'
    })

    response = client.post('/customer/login', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'You are login now!' in response.data

# Test for customer logout
def test_customer_logout(client):
    # Register and login a user first
    client.post('/customer/register', data={
        'name': 'Test User',
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'country': 'Testland',
        'city': 'Testville',
        'contact': '1234567890',
        'address': '123 Test St',
        'zipcode': '12345'
    })
    client.post('/customer/login', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    })

    response = client.get('/customer/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You have been logged out.' in response.data  # Adjust based on actual message

# Test for placing an order
def test_get_order(client):
    # Register and login a user first
    client.post('/customer/register', data={
        'name': 'Test User',
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'country': 'Testland',
        'city': 'Testville',
        'contact': '1234567890',
        'address': '123 Test St',
        'zipcode': '12345'
    })
    client.post('/customer/login', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    })

    with client.session_transaction() as session:
        session['Shoppingcart'] = {'1': {'name': 'Test Product', 'price': '10.00', 'quantity': '1', 'discount': '0'}}

    response = client.get('/getorder', follow_redirects=True)
    assert response.status_code == 200
    assert b'Your order has been sent successfully' in response.data

# Test for viewing order details
def test_orders(client):
    # Register and login a user first
    client.post('/customer/register', data={
        'name': 'Test User',
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'country': 'Testland',
        'city': 'Testville',
        'contact': '1234567890',
        'address': '123 Test St',
        'zipcode': '12345'
    })
    client.post('/customer/login', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    })

    # Create an order
    with client.session_transaction() as session:
        session['Shoppingcart'] = {'1': {'name': 'Test Product', 'price': '10.00', 'quantity': '1', 'discount': '0'}}
    client.get('/getorder', follow_redirects=True)

    # Get the invoice from the order
    order = CustomerOrder.query.filter_by(customer_id=1).first()
    invoice = order.invoice

    response = client.get(f'/orders/{invoice}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Order Details' in response.data  # Adjust based on actual content

# Test for generating PDF of an order
def test_get_pdf(client):
    # Register and login a user first
    client.post('/customer/register', data={
        'name': 'Test User',
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'country': 'Testland',
        'city': 'Testville',
        'contact': '1234567890',
        'address': '123 Test St',
        'zipcode': '12345'
    })
    client.post('/customer/login', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    })

    # Create an order
    with client.session_transaction() as session:
        session['Shoppingcart'] = {'1': {'name': 'Test Product', 'price': '10.00', 'quantity': '1', 'discount': '0'}}
    client.get('/getorder', follow_redirects=True)

    # Get the invoice from the order
    order = CustomerOrder.query.filter_by(customer_id=1).first()
    invoice = order.invoice

    response = client.post(f'/get_pdf/{invoice}', follow_redirects=True)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/pdf'

# Test for viewing order history
def test_customer_orders(client):
    # Register and login a user first
    client.post('/customer/register', data={
        'name': 'Test User',
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'country': 'Testland',
        'city': 'Testville',
        'contact': '1234567890',
        'address': '123 Test St',
        'zipcode': '12345'
    })
    client.post('/customer/login', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    })

    # Create an order
    with client.session_transaction() as session:
        session['Shoppingcart'] = {'1': {'name': 'Test Product', 'price': '10.00', 'quantity': '1', 'discount': '0'}}
    client.get('/getorder', follow_redirects=True)

    response = client.get('/customer/orders', follow_redirects=True)
    assert response.status_code == 200
    assert b'Order History' in response.data  # Adjust based on actual content
