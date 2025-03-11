from flask import render_template, session, redirect,request,url_for,flash
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from.models import User
from shop.products.models import Addproduct,Brand,Category
from ..customer.models import CustomerOrder 
import os 
import json








@app.route('/admin')
def admin():
   if 'email' not in session:
      flash(f'login first please','danger')
      return redirect(url_for('login'))
   products =Addproduct.query.all()
   return render_template('admin/index.html',title='Admin Page ',products=products)


@app.route('/brands')
def brands():
    if 'email'not in session:
       flash(f'you should be login to contenu ','danger')
       return redirect('login')
    brands=Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html' ,title="Brands",brands=brands)

@app.route('/category')
def category():
   if 'email'not in session:
      flash(f'your should be logiin to continue')
      return redirect(url_for('login'))
   categorys=Category.query.order_by(Category.id.desc()).all()
   return render_template('admin/brand.html' ,title='Category',categorys=categorys)


@app.route('/register',methods=['GET','POST'])
def register():
 form = RegistrationForm()
 if form.validate_on_submit():
    hash_password= bcrypt.generate_password_hash(form.password.data)
    user=User(name=form.name.data,username=form.username.data,email=form.email.data,password=hash_password)
    db.session.add(user)
    db.session.commit()
    flash(f'Welcom {form.name.data} Thank you for Registering ','success')
    return redirect(url_for('login'))
 return render_template('admin/register.html', title='Registier page', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'welcome {form.email.data} you are logedin now','success')
            return redirect(url_for('admin'))
        else:
            flash(f'Wrong email and password', 'success')
            return redirect(url_for('login'))
    return render_template('admin/login.html',title='Login page',form=form)
   

@app.route('/logout')
def logout():
    session.pop('email', None)  # Remove user from session
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('login'))

    
@app.route('/admin/orders')
def admin_orders():
    if 'email' not in session:  # Check if the admin is logged in
        flash('Please log in first!', 'danger')
        return redirect(url_for('login'))

    orders = CustomerOrder.query.order_by(CustomerOrder.date_created.desc()).all()  # Get all orders

    return render_template('admin/orders.html', title='All Orders', orders=orders)

# @app.route('/admin/order/<int:order_id>')
# def view_order(order_id):
#     if 'email' not in session:
#         flash('Please log in first!', 'danger')
#         return redirect(url_for('login'))

#     order = CustomerOrder.query.get_or_404(order_id)  # Get order by ID
#     return render_template('admin/order_details.html', order=order)
@app.route('/admin/order/<int:order_id>')
def view_order(order_id):
    # Check if admin is logged in. Handle if session is not active.
    if 'email' not in session:
        flash('Please log in first!', 'danger')
        return redirect(url_for('login'))
    
    order = CustomerOrder.query.get_or_404(order_id)

    # Retrieve the customer by customer_id
    customer = CustomerOrder.query.get(order.customer_id)  # Adjust this as per your actual model and field names
    
    # Check if order.orders is a string (then we can parse it)
    if isinstance(order.orders, str):
        try:
            order_details = json.loads(order.orders)
        except json.JSONDecodeError:
            order_details = []
    else:
        order_details = order.orders if isinstance(order.orders, list) else []
    
    return render_template('admin/order_details.html', order=order, order_details=order_details, customer=customer)

