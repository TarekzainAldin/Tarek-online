import os
import pytest
from shop import db, app
from shop.products.models import Brand, Category, Addproduct
from shop.admin.models import User  # Assuming you have a User model for authentication
from werkzeug.security import generate_password_hash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)  # Initialize Bcrypt with the app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-memory database

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


@pytest.fixture
def test_image():
    """Create a temporary test image.""" 
    filename = "test_image.jpg"
    with open(filename, "wb") as f:
        f.write(os.urandom(1024))  # Generate a 1KB random file
    yield filename
    os.remove(filename)  # Clean up


@pytest.fixture
def test_user():
    """Create a test user for authentication."""
    # Generate password hash using bcrypt
    hashed_password = bcrypt.generate_password_hash("password").decode('utf-8')  
    print(f"Hashed Password: {hashed_password}")  # Add this line for debugging
    user = User(
        name="Test User",
        username="testuser123",  # Ensure this is unique for each test
        email="test@example.com",
        password=hashed_password,  # Store the bcrypt hashed password
    )
    db.session.add(user)
    db.session.commit()
    return user


def test_add_product(client, test_image, test_user):
    """Test adding a new product with authentication."""
    # Log in as the test user
    response = client.post('/login', data={'email': test_user.email, 'password': 'password'})
    
    # Check if the login response is a redirect (302)
    assert response.status_code == 302
    
    # Follow the redirect to the next page (usually the dashboard or homepage)
    location = response.headers['Location']
    response = client.get(location)

    # Ensure that you're logged in and redirected to the right page
    assert b"Welcome" in response.data  # Adjust this to match your app's behavior after login (e.g., a welcome message)

    # Ensure that you're in the correct app context to perform database operations
    with app.app_context():
        # Create a brand and category
        brand = Brand(name="New Brand")
        category = Category(name="New Category")
        db.session.add(brand)
        db.session.add(category)
        db.session.commit()

        # Fetch the created brand and category from the database
        brand = db.session.query(Brand).filter_by(name="New Brand").first()
        category = db.session.query(Category).filter_by(name="New Category").first()

        # Add a new product with the generated test image
        product = Addproduct(
            name="New Product",
            price=100,
            discount=10,
            stock=50,
            colors="Red",
            desc="New Product Description",
            brand_id=brand.id,
            category_id=category.id,
            image_1="test_image.jpg",
            image_2="test_image.jpg",
            image_3="test_image.jpg",
        )

        db.session.add(product)
        db.session.commit()

        # Now that product is added, let's assert it's in the database
        product = db.session.query(Addproduct).filter_by(name="New Product").first()
        assert product is not None

    # Check if the product appears in the response after adding it
    response = client.get('/')  # Access the homepage instead of /products

    # Debugging: print out the response data
    print(response.data)  # This will print out the raw HTML of the response for debugging

    # Assert that "New Product" is in the response data (indicating the product was added successfully)
    assert b"New Product" in response.data

