from flask import render_template , session , redirect , request, url_for
from shop import app,db

@app.route('/')
def home():
    return render_template('layout.html',title='Tarek-online')

@app.route('/register')
def register():
    return render_template('admin/register.html', title ="Register user")