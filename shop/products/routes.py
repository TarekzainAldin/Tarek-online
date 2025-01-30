from flask import redirect ,render_template, session, url_for, flash, request,current_app
from shop import db , app ,photos
from .models import Brand, Category,Addproduct
from .forms import Addproducts
import secrets
import os 
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

@app.route('/deletebrand/<int:id>', methods=['GET','POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        flash(f"The brand {brand.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"The brand {brand.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))




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
        return redirect(url_for('category'))
    category = updatecat.name
    return render_template('products/updatebrand.html', title='Update cat',updatecat=updatecat)

@app.route('/deletecat/<int:id>', methods=['GET','POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        flash(f"The brand {category.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"The brand {category.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))


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


@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):  
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.all()
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = Addproducts(request.form)
    
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.stock = form.stock.data
        product.colors = form.colors.data
        product.desc = form.desc.data
        
        # Handling image_1 upload
        if request.files.get('image_1'):
            try:  
                os.unlink(os.path.join(current_app.root_path, "static/images", product.image_1))  # Correct path
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except Exception as e:
                print(f"Error deleting image_1: {e}")
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        
        # Handling image_2 upload
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images", product.image_2))  # Correct path
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except Exception as e:
                print(f"Error deleting image_2: {e}")
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        
        # Handling image_3 upload
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images", product.image_3))  # Correct path
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except Exception as e:
                print(f"Error deleting image_3: {e}")
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        
        db.session.commit()
        flash('Your product has been updated successfully!', 'success')
        return redirect(url_for('admin'))
   
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.desc.data = product.desc 

    return render_template('products/updateproduct.html', title="Update Product", form=form, brands=brands, categories=categories, product=product)