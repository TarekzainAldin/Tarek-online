from flask import redirect ,render_template, session, url_for, flash, request
from shop import db , app ,photos
from .models import Brand, Category,Addproduct
from .forms import Addproducts
import secrets

@app.route('/addbrand',methods=['GET','POST'])
def addbrand():
    if request.method =="POST":
        getbrand=request.form.get('brand')
        brand=Brand(name=getbrand)
        db.session.add(brand)
        flash(f'brand "{getbrand}" added successfully!','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html',brands='brands')


# @app.route('/update_brand/<int:id>',methods=['GET','POST'])
# def update_brand(id):
#     if 'email' not in session:
#         flash(f'should be login first','danger')
#         updatebrand=Brand.query.get_or_404(id)
#         brand=request.form.get('brand')
#         if request.method=="POST":
#          updatebrand.name=brand
#          flash(f'your brand has been updated','success')
#          db.session.commit()
#          return redirect(url_for('brands'))
#     return render_template('products/updatebrand.html',title='UPDATE BRAND',updatebrand=updatebrand)


@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash('Login first please','danger')
       
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method =="POST":
        updatebrand.name = brand
        flash(f'The brand {updatebrand.name} was changed to {brand}','success')
        db.session.commit()
        return redirect(url_for('brands'))
    brand = updatebrand.name
    return render_template('products/updatebrand.html', title='Udate brand',updatebrand=updatebrand)





@app.route('/addcat',methods=['GET','POST'])
def addcat():
    if request.method =="POST":
        getcat = request.form.get('category')
        category = Category(name=getcat)
        db.session.add(category)
        flash(f'The brand {getcat} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html', title='Add category')


# @app.route('/updatecat/<int:id>',methods=['GET','POST'])
# def updatecat(id):
#     if 'email' not in session:
#          flash(f'should be in login for make update','danger')
#     updatecat=Category.query.get_or_404(id)
#     category=request.form.get('category')
#     if request.method=="post":
#          updatecat.name=category
#          flash(f'your category has been updated success!','success')
#          db.session.commit()
#          return redirect(url_for("category"))
#     return render_template('products/updatebrand.html', title="update category page", updatecat=updatecat)


@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')  
    if request.method =="POST":
        updatecat.name = category
        flash(f'The category {updatecat.name} was changed to {category}','success')
        db.session.commit()
        return redirect(url_for('categories'))
    category = updatecat.name
    return render_template('products/addbrand.html', title='Update cat',updatecat=updatecat)

@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    form = Addproducts(request.form)
    brands = Brand.query.all()
    categories = Category.query.all()
    if request.method == "POST" and 'image_1' in request.files:
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.desc.data  # Correct field name here
        brand = request.form.get('brand')
        category = request.form.get('category')
        
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        
        # Use 'discription' instead of 'desc'
        addproduct = Addproduct(
            name=name,
            price=price,
            discount=discount,
            stock=stock,
            colors=colors,
            desc=desc,  # Use 'discription' here
            category_id=category,
            brand_id=brand,
            image_1=image_1,
            image_2=image_2,
            image_3=image_3
        )
        
        db.session.add(addproduct)
        flash(f'The product {name} was added in database', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', form=form, title='Add a Product', brands=brands, categories=categories)
