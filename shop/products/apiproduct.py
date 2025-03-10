from decimal import Decimal
from flask import Flask, jsonify, request, session, current_app
from shop import app, db, photos
from .models import Category, Brand, Addproduct
import os
from werkzeug.utils import secure_filename

# Helper function to convert models to dictionaries
def to_dict(model_instance):
    result = {}
    for column in model_instance.__table__.columns:
        value = getattr(model_instance, column.name)
        
        if isinstance(value, Decimal):
            result[column.name] = float(value)
        else:
            result[column.name] = value
    return result

# Standardized response for API
def make_response(status, message, data=None):
    response = {'status': status, 'message': message}
    if data:
        response['data'] = data
    return jsonify(response)

# API Routes - Admin

# Brands
@app.route('/api/admin/brands', methods=['GET'])
def api_brands():
    if 'email' not in session:
        return make_response('error', 'You must be logged in to continue.'), 401
    brands = Brand.query.order_by(Brand.id.desc()).all()
    brands_list = [to_dict(brand) for brand in brands]
    return make_response('success', 'Brands fetched successfully', brands_list)

@app.route('/api/admin/addbrands', methods=['POST'])
def api_add_brand():
    if 'email' not in session:
        return make_response('error', 'Login first please'), 401
    data = request.get_json()
    name = data.get('name')
    brand = Brand(name=name)
    db.session.add(brand)
    db.session.commit()
    return make_response('success', f'Brand {name} added successfully!')



@app.route('/api/admin/updatebrands/<int:id>', methods=['PUT'])
def api_update_brand(id):
    # Ensure the user is logged in
    if 'email' not in session:
        return jsonify({'message': 'Login first please', 'status': 'error'}), 401
    
    # Retrieve the brand by its ID, if it doesn't exist, return a 404 error
    brand = Brand.query.get_or_404(id)

    # Get the data from the request body
    data = request.get_json()

    # Validate the request data
    if not data or not data.get('name'):
        return jsonify({'message': 'Brand name is required.', 'status': 'error'}), 400

    # Update the brand's name
    brand.name = data['name']

    # Commit the changes to the database
    try:
        db.session.commit()
        return jsonify({'message': f'Brand {brand.name} updated successfully!', 'status': 'success'}), 200
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of error
        return jsonify({'message': f'An error occurred: {str(e)}', 'status': 'error'}), 500



@app.route('/api/admin/deletebrands/<int:id>', methods=['DELETE'])
def api_delete_brand(id):
    if 'email' not in session:
        return make_response('error', 'Login first please'), 401
    brand = Brand.query.get_or_404(id)
    db.session.delete(brand)
    db.session.commit()
    return make_response('success', f'Brand {brand.name} deleted successfully!')

# Categories
@app.route('/api/admin/categories', methods=['GET'])
def api_categories():
    if 'email' not in session:
        return make_response('error', 'Login first please'), 401
    categories = Category.query.all()
    categories_list = [to_dict(category) for category in categories]
    return make_response('success', 'Categories fetched successfully', categories_list)

@app.route('/api/admin/addcategories', methods=['POST'])
def api_add_category():
    if 'email' not in session:
        return make_response('error', 'Login first please'), 401
    data = request.get_json()
    name = data.get('name')
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return make_response('success', f'Category {name} added successfully!')

@app.route('/api/admin/updatecategories/<int:id>', methods=['PUT'])
def api_update_category(id):
    if 'email' not in session:
        return make_response('error', 'Login first please'), 401
    category = Category.query.get_or_404(id)
    data = request.get_json()
    category.name = data.get('name', category.name)
    db.session.commit()
    return make_response('success', f'Category {category.name} updated successfully!')

@app.route('/api/admin/deletecategories/<int:id>', methods=['DELETE'])
def api_delete_category(id):
    if 'email' not in session:
        return make_response('error', 'Login first please'), 401
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return make_response('success', f'Category {category.name} deleted successfully!')

# Products
@app.route('/api/admin/products', methods=['GET'])
def api_products():
    if 'email' not in session:
        return make_response('error', 'Login first please'), 401
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=8)
    products_list = [to_dict(product) for product in products.items]
    return make_response('success', 'Products fetched successfully', {
        'products': products_list,
        'total': products.total,
        'pages': products.pages
    })

@app.route('/api/admin/singleproducts/<int:id>', methods=['GET'])
def api_single_product(id):
    if 'email' not in session:
        return make_response('error', 'Login first please'), 401
    product = Addproduct.query.get_or_404(id)
    return make_response('success', 'Product fetched successfully', to_dict(product))


import base64
import os
from flask import request, jsonify
from shop import app, db
from shop.products.models import Addproduct
from shop.admin.models import User

UPLOAD_FOLDER = 'static/images/'  # Set your upload folder path
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload folder exists

def save_base64_image(base64_string, filename):
    """Helper function to save base64-encoded images"""
    try:
        image_data = base64.b64decode(base64_string)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as f:
            f.write(image_data)
        return file_path
    except Exception as e:
        return None

@app.route('/api/admin/addproducts', methods=['POST'])
def api_add_product():
    if 'email' not in session:
        return jsonify({'message': 'Login first please', 'status': 'error'}), 401

    data = request.get_json()

    # Extract required fields
    required_fields = ['name', 'price', 'brand_id', 'category_id']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return jsonify({'message': f'Missing required fields: {", ".join(missing_fields)}', 'status': 'error'}), 400

    # Save base64 images if provided
    image_1_path = save_base64_image(data.get('image_1'), "image_1.jpg") if data.get('image_1') else None
    image_2_path = save_base64_image(data.get('image_2'), "image_2.jpg") if data.get('image_2') else None
    image_3_path = save_base64_image(data.get('image_3'), "image_3.jpg") if data.get('image_3') else None

    # Create product
    new_product = Addproduct(
        name=data['name'],
        price=data['price'],
        discount=data.get('discount', 0),
        stock=data.get('stock', 0),
        colors=data.get('colors', ''),
        desc=data.get('desc', ''),
        brand_id=data['brand_id'],
        category_id=data['category_id'],
        image_1=image_1_path,
        image_2=image_2_path,
        image_3=image_3_path
    )

    try:
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': f'Product {data["name"]} added successfully!', 'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Database error', 'status': 'error', 'error': str(e)}), 500



UPLOAD_FOLDER = 'static/images/'  
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  

def save_base64_image(base64_string, filename):
    """Helper function to save base64-encoded images"""
    try:
        if not base64_string:
            return None  # Return None if the image is not provided
        
        image_data = base64.b64decode(base64_string)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as f:
            f.write(image_data)
        return file_path
    except Exception as e:
        return None

@app.route('/api/admin/updateproducts/<int:id>', methods=['PUT'])
def api_update_product(id):
    if 'email' not in session:
        return jsonify({'message': 'Login first please', 'status': 'error'}), 401
    
    product = Addproduct.query.get_or_404(id)
    data = request.get_json()

    # Update text fields
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.discount = data.get('discount', product.discount)
    product.stock = data.get('stock', product.stock)
    product.colors = data.get('colors', product.colors)
    product.desc = data.get('desc', product.desc)
    product.brand_id = data.get('brand_id', product.brand_id)
    product.category_id = data.get('category_id', product.category_id)

    # Update images only if new ones are provided, otherwise keep existing ones
    product.image_1 = save_base64_image(data.get('image_1'), f"product_{id}_1.jpg") or product.image_1
    product.image_2 = save_base64_image(data.get('image_2'), f"product_{id}_2.jpg") or product.image_2
    product.image_3 = save_base64_image(data.get('image_3'), f"product_{id}_3.jpg") or product.image_3

    try:
        db.session.commit()
        return jsonify({'message': f'Product {product.name} updated successfully!', 'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Database error', 'status': 'error', 'error': str(e)}), 500

@app.route('/api/admin/deleteproducts/<int:id>', methods=['DELETE'])
def api_delete_product(id):
    if 'email' not in session:
        return make_response('error', 'Login first please'), 401
    product = Addproduct.query.get_or_404(id)

    try:
        os.unlink(os.path.join(current_app.root_path, "static/images", product.image_1))
        os.unlink(os.path.join(current_app.root_path, "static/images", product.image_2))
        os.unlink(os.path.join(current_app.root_path, "static/images", product.image_3))
    except Exception as e:
        print(e)
    
    db.session.delete(product)
    db.session.commit()

    return make_response('success', f'Product {product.name} deleted successfully!')
