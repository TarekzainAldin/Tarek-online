from flask import render_template , session , redirect , request, url_for,flash 
from shop import app,db,bcrypt
from.forms import RegistrationForm
from .models import User
import os 


@app.route('/')
def home():
    return render_template('admin/index.html',title='Tarek-online')
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data}, Thanks for registering!', 'success')
        
        return redirect(url_for('home'))
    return render_template('admin/register.html', title='Register User', form=form)
