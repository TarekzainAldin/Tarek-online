from flask import jsonify, request, session, make_response, flash, redirect, url_for ,render_template
from flask_login import login_required, current_user, login_user, logout_user
from shop import app, db, bcrypt
from .models import Register, CustomerOrder
from shop.customer.forms import CustomerRegisterForm, CustomerLoginForm
import secrets
import stripe
import pdfkit

stripe.api_key = 'sk_test_51MTmW1LeR5YvDcaB7I1SK4DCiiO8frI1ChvtXS55bPb2srgwFmjjGIOV3I0BEjqJ1Rb2UPZ9f37KCeG9HAhjk0Pg00NSicw8tm'

@app.route('/api/customer/register', methods=['POST'])
def api_customer_register():
    """
    Customer Registration
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    country = data.get('country')
    city = data.get('city')
    contact = data.get('contact')
    address = data.get('address')
    zipcode = data.get('zipcode')

    if not all([name, username, email, password, country, city, contact, address, zipcode]):
        return jsonify({"error": "All fields are required"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        new_user = Register(
            name=name,
            username=username,
            email=email,
            password=hashed_password,
            country=country,
            city=city,
            contact=contact,
            address=address,
            zipcode=zipcode
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/customer/login', methods=['POST'])
def api_customer_login():
    """
    Customer Login
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = Register.query.filter_by(email=email).first()
    
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid email or password"}), 401

@app.route('/api/customer/logout', methods=['GET'])
@login_required
def api_customer_logout():
    """
    Customer Logout
    """
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/api/customer/orders', methods=['GET'])
@login_required
def api_customer_orders():
    """
    Get Customer's Order History
    """
    orders = CustomerOrder.query.filter_by(customer_id=current_user.id).all()

    if not orders:
        return jsonify({"message": "No orders found"}), 404

    order_list = []
    for order in orders:
        subTotal = 0
        for product in order.orders.values():
            subTotal += float(product['price']) * int(product['quantity'])
        
        tax = subTotal * 0.06  # Assuming a 6% tax rate
        grandTotal = subTotal + tax

        order_list.append({
            'invoice': order.invoice,
            'status': order.status,
            'date_created': order.date_created,
            'total_amount': round(grandTotal, 2)
        })
    
    return jsonify({"orders": order_list}), 200


@app.route('/api/customer/order/<invoice>', methods=['GET'])
@login_required
def api_get_order_details(invoice):
    """
    Get Details of a Specific Order
    """
    order = CustomerOrder.query.filter_by(customer_id=current_user.id, invoice=invoice).first()

    if not order:
        return jsonify({"error": "Order not found"}), 404

    # Calculate total_amount based on the order items in the `orders` JSON field
    total_amount = 0
    if isinstance(order.orders, dict):
        for item in order.orders.values():
            total_amount += float(item.get('price', 0)) * int(item.get('quantity', 0))
    
    order_data = {
        'invoice': order.invoice,
        'status': order.status,
        'date_created': order.date_created,
        'orders': order.orders,
        'total_amount': total_amount  # Use the calculated total_amount here
    }

    return jsonify({"order": order_data}), 200
@app.route('/api/payment', methods=['POST'])
def api_payment():
    """
    Stripe Payment API
    """
    data = request.get_json()

    invoice = data.get('invoice')
    amount = data.get('amount')

    # Fetch order from database
    orders = CustomerOrder.query.filter_by(customer_id=current_user.id, invoice=invoice).first()

    if not orders:
        return jsonify({"error": "Order not found"}), 404

    order_data = orders.orders  # Assuming orders are stored as JSON field

    if not isinstance(order_data, dict):
        return jsonify({"error": "Invalid order format"}), 400

    product_names = ", ".join([item["name"] for item in order_data.values()])
    order_description = f"Order #{orders.invoice}: {product_names}"

    try:
        # Create Stripe customer
        customer = stripe.Customer.create(
            email=data.get('stripeEmail'),
            source=data.get('stripeToken')
        )

        # Create Stripe charge
        charge = stripe.Charge.create(
            customer=customer.id,
            description=order_description,
            amount=amount,
            currency='usd',
        )

        # Mark order as paid
        orders.status = 'Paid'
        db.session.commit()

        return jsonify({"message": "Payment successful, order marked as paid"}), 200
    except stripe.error.StripeError as e:
        return jsonify({"error": f"Payment failed: {e.user_message}"}), 400

@app.route('/api/customer/order/pdf/<invoice>', methods=['GET'])
@login_required
def api_generate_pdf(invoice):
    """
    Generate PDF Invoice for an Order
    """
    order = CustomerOrder.query.filter_by(customer_id=current_user.id, invoice=invoice).first()

    if not order:
        return jsonify({"error": "Order not found"}), 404

    # Assuming tax and subtotal calculations
    subTotal = 0
    grandTotal = 0
    for product in order.orders.values():
        subTotal += float(product['price']) * int(product['quantity'])
    grandTotal = subTotal * 1.06  # Assuming a 6% tax rate

    rendered = render_template('customer/pdf.html', invoice=invoice, order=order, subTotal=subTotal, grandTotal=grandTotal)

    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename={invoice}.pdf'
    
    return response
