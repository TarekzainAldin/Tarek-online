from flask import jsonify, request, session, flash, redirect, url_for
from shop import app, db, bcrypt
from shop.products.models import Addproduct, Brand, Category
from shop.customer.models import CustomerOrder
from shop.admin.models import User
from shop.admin.forms import RegistrationForm, LoginForm
from decimal import Decimal


# Helper function to convert objects to dictionaries
def to_dict(model_instance):
    result = {}
    for column in model_instance.__table__.columns:
        value = getattr(model_instance, column.name)
        
        # Convert Decimal to float
        if isinstance(value, Decimal):
            result[column.name] = float(value)
        else:
            result[column.name] = value

    return result

from flask import jsonify

@app.route('/api/admin/brands', methods=['GET'])
def api_admin_brands():  # Renamed function
    if 'email' not in session:
        return jsonify({"message": "You must be logged in to continue."}), 401
    brands = Brand.query.order_by(Brand.id.desc()).all()
    
    brands_list = []
    for brand in brands:
        brand_data = {"id": brand.id, "name": brand.name}
        # Check if 'description' exists as an attribute
        if hasattr(brand, 'description'):
            brand_data["description"] = brand.description
        
        brands_list.append(brand_data)

    return jsonify(brands_list)


@app.route('/api/admin/category', methods=['GET'])
def api_admin_category():  # Renamed function
    if 'email' not in session:
        return jsonify({"message": "You must be logged in to continue."}), 401
    categories = Category.query.order_by(Category.id.desc()).all()
    
    categories_list = []
    for category in categories:
        category_data = {"id": category.id, "name": category.name}
        # Check if 'description' exists as an attribute
        if hasattr(category, 'description'):
            category_data["description"] = category.description
        
        categories_list.append(category_data)

    return jsonify(categories_list)


# ✅ Change route name to avoid conflict
@app.route('/api/admin/dashboard', methods=['GET'])
def admin_dashboard_api():  # Renamed function
    if 'email' not in session:
        return jsonify({'message': 'Unauthorized access. Please log in.', 'status': 'error'}), 401
    products = Addproduct.query.all()
    return jsonify({'status': 'success', 'products': [to_dict(product) for product in products]})


# ✅ API Login
@app.route('/api/admin/login', methods=['POST'])
def api_admin_login():  # Renamed function
    # Attempt to get the JSON data from the request
    data = request.get_json()

    # Check if the data is None, which means invalid JSON or missing data
    if not data:
        return jsonify({'message': 'Invalid JSON or empty request body.', 'status': 'error'}), 400

    # Now it's safe to access 'email' and 'password' from 'data'
    user = User.query.filter_by(email=data.get('email')).first()

    if user and bcrypt.check_password_hash(user.password, data.get('password')):
        session['email'] = user.email
        return jsonify({'message': f'Welcome {user.email}, you are logged in now!', 'status': 'success'})
    else:
        return jsonify({'message': 'Invalid credentials', 'status': 'error'}), 401


# ✅ API Logout
@app.route('/api/admin/logout', methods=['GET'])
def api_admin_logout():  # Renamed function
    session.pop('email', None)
    return jsonify({'message': 'You have been logged out successfully!', 'status': 'success'})


# ✅ Get all orders
@app.route('/api/admin/orders', methods=['GET'])
def api_admin_orders():  # Renamed function
    if 'email' not in session:
        return jsonify({'message': 'Unauthorized access. Please log in.', 'status': 'error'}), 401
    
    orders = CustomerOrder.query.order_by(CustomerOrder.date_created.desc()).all()
    return jsonify({'status': 'success', 'orders': [to_dict(order) for order in orders]})


# ✅ Get a single order
@app.route('/api/admin/order/<int:order_id>', methods=['GET'])
def api_admin_view_order(order_id):  # Renamed function
    if 'email' not in session:
        return jsonify({'message': 'Unauthorized access. Please log in.', 'status': 'error'}), 401
    
    order = CustomerOrder.query.get_or_404(order_id)
    return jsonify({'status': 'success', 'order': to_dict(order)})
