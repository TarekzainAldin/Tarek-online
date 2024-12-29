from flask import render_template , session , redirect , request, url_for,flash
from shop import app,db
from.forms import RegistrationForm

@app.route('/')
def home():
    return render_template('layout.html',title='Tarek-online')

@app.route('/register',methods = ['GET','POST'])
def register():
    form=RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('you have been registered successfully ')
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form, title='REGISTER')