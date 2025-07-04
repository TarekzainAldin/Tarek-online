Tarek online
# E-Commerce Platform

A full-featured e-commerce platform built with Flask featuring product management, customer accounts, shopping cart, and Stripe payment integration.

## Table of Contents
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Models](#database-models)
- [API Routes](#api-routes)
- [Admin Panel](#admin-panel)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Features

### Core Functionality
- 🛒 Product catalog with categories/brands
- 🔍 Product search functionality
- 👤 User authentication (Admin/Customer)
- 🛒 Shopping cart system
- 💳 Stripe payment integration
- 📦 Order management system

### Admin Features
- 📊 Dashboard with analytics
- ➕ Add/Edit/Delete products
- 🏷️ Manage categories & brands
- 📝 View all customer orders
- 📊 Inventory management

### Customer Features
- 👤 Account registration
- 📜 Order history
- 📄 PDF invoice generation
- 🔒 Secure checkout process
- 📱 Responsive design

## Technologies

### Backend
- Python 3.9+
- Flask 2.0
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- Flask-Bcrypt

### Frontend
- Bootstrap 5
- Jinja2 Templating
- JavaScript

### Database
- SQLite (Development)
- PostgreSQL (Production-ready)

### APIs
- Stripe Payment API

## Installation

### Prerequisites
- Python 3.9+
- pip package manager

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/TarekzainAldin/Tarek-online.git
   cd ecommerce-flask


Create and activate virtual environment:
  python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows


Install dependencies:
pip install -r requirements.txt

Initialize database:
   flask db init
flask db migrate -m "Initial migration"
flask db upgrade

Run the application:
flask run

Configration 
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///Tarek-online.db
STRIPE_PUBLIC_KEY=your_stripe_pk
STRIPE_SECRET_KEY=your_stripe_sk
UPLOAD_FOLDER=./static/images



Database Models

here i need but photo 



API Routes
Admin Routes
Endpoint	Method	Description
/admin	GET	Admin dashboard
/addbrand	GET,POST	Add new brand
/addcat	GET,POST	Add new category
/addproduct	GET,POST	Add new product
/updateproduct/<id>	GET,POST	Update product
/deleteproduct/<id>	POST	Delete product



   Customer Routes
Endpoint	Method	Description
/customer/register	GET,POST	Customer registration
/customer/login	GET,POST	Customer login
/getorder	GET	Process order
/orders/<invoice>	GET	View order details



Product Routes
Endpoint	Method	Description
/	GET	Home page
/product/<id>	GET	Product details
/brand/<id>	GET	Products by brand
/categories/<id>	GET	Products by category
Admin Panel
Product Management
https://via.placeholder.com/600x400?text=Product+Management

Add/edit/delete products

Upload multiple images

Set pricing and discounts

Manage inventory levels

Order Management
https://via.placeholder.com/600x400?text=Order+Management

View all customer orders

See detailed order information

Track order status

Generate invoices

License
Distributed under the MIT License. See LICENSE for more information.

