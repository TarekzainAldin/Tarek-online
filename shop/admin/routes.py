from flask import render_template, session, redirect,request,url_for,flash
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from.models import User
from shop.products.models import Addproduct,Brand,Category
from ..customer.models import CustomerOrder 
import os 




# @app.route('/')
# def home_page():
#     page=request.args.get('page',1,type=int)
#     products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page,per_page=1)
#     brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
#     categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()  # Fix `.all()`
    
#     return render_template(
#         'products/index.html',
#         title='Product Page',
#         products=products,
#         brands=brands,
#         categories=categories  # Fix variable name
#     )

# @app.route('/brand/<int:id>')
# def get_brand(id):
#     brand_products = Addproduct.query.filter_by(brand_id=id).all()
#     brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
#     categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
#     return render_template(
#         'products/index.html',
#         title='Brand Products',
#         products=brand_products,  # Ensure template expects `products`
#         brands=brands,
#         categories=Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()  # Include categories for consistency
#     )

# @app.route('/categories/<int:id>')
# def get_categories(id):
#     get_cat_prod = Addproduct.query.filter_by(category_id=id).all()  # Fix typo (`guery` → `query`)
#     categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()  # Fix `.all()`
#     brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
#     return render_template(
#         'products/index.html',
#         title='Category Products',
#         products=get_cat_prod,  # Ensure template expects `products`
#         brands=Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all(),  # Include brands for consistency
#         categories=categories
#     )

# @app.route('/')
# def home_page():
#     products=Addproduct.query.filter(Addproduct.stock>0)
#     brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
#     categorys=Category.query.join(Addproduct,(Category.id== Addproduct.category_id)).all
#     return render_template('products/index.html' ,title='Product page' ,products=products,brands=brands,categorys=categorys)

# @app.route('/brand/<int:id>')
# def get_brand(id):
#    brand=Addproduct.query.filter_by(brand_id=id)
#    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
#    return render_template('products/index.html',brand=brand,brands=brands)



# @app.route('/categories/<int:id>')
# def get_categories(id):
#    get_cat_prod=Addproduct.guery.filter_by(category_id=id)
#    categorys=Category.query.join(Addproduct,(category.id== Addproduct.category_id)).all
#    return render_template('/products/index.html',get_cat_prod=get_cat_prod,categorys=categorys)



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

@app.route('/admin/order/<int:order_id>')
def view_order(order_id):
    if 'email' not in session:
        flash('Please log in first!', 'danger')
        return redirect(url_for('login'))

    order = CustomerOrder.query.get_or_404(order_id)  # Get order by ID
    return render_template('admin/order_details.html', order=order)
