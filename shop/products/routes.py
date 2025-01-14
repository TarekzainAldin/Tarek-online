from flask import redirect ,render_template, session, url_for, flash, request
from shop import db , app 
from .models import Brand, Category
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
# def updatecat():
#     if email not in session:
#         flash(f"plase login first",'danger')
#     updatecat =Category.query.get_or_404(id)
#     category=request.form.get('category')
#     if request.method=='POST':
#         updatecat.name=category
#         flash(f"your category has been updateing {category}",'success')
#         db.session.commit()
#         return redirect(url_for('category'))
#     return render_template('producs/updatebrand.html')


@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
     brands=Brand.query.all()
     categorys=Category.query.all()
     form=Addproducts(request.form)
     return render_template('products/addproduct.html',title="Add Product", form=form,brands=brands, categorys=categorys)

