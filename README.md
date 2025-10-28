🚗 Car Showroom Management System

A full-stack Django web application that manages car sales, trade-ins, and customer data.
Built with Django, Django REST Framework (DRF), and Bootstrap, this project demonstrates authentication, RESTful APIs, role-based access, and relational data modeling.

🌟 Features
🔐 Authentication & Roles

Custom User model with roles (Admin, Sales, Customer)

Secure login & registration using Django auth

Role-based permission classes (Admin or Sales-only actions)

(Optionally) JWT authentication via djangorestframework-simplejwt

🚘 Cars Management

CRUD operations for car listings

Filtering by brand, year, price, and transmission

Image upload & management

API endpoints for integration with frontends (React or plain HTML)

👥 Customers Management

Add, edit, delete customer profiles

Search and filter by name, phone, or status

REST API with pagination and search filter support

Bootstrap-based responsive frontend

🛒 Orders & Trade-In

Create and manage car orders linked to customers

Support trade-in cars with valuation fields

Nested serializers to return related data in a single API call

Order workflow with status (Pending → Confirmed → Completed)



🧱 Project Structure
carShowRoom/
├── carShowRoom/           # Main project config (settings, urls)
├── users/                 # Authentication & roles
├── customer/              # Customer data management
├── cars/                  # Car models and listings
├── orders/                # Orders, trade-ins, and sales flow
├── demo/                  # Demo
├── static/                # Static assets (Bootstrap, JS)
├── templates/             # HTML templates
└── requirements.txt

⚙️ Tech Stack
Layer	Technology
Backend	    Django 5.x, Django REST Framework
Frontend	Bootstrap 5, Vanilla JS
Auth	    Django Auth / JWT (SimpleJWT)
Database	SQLite (development)
Docs	    drf-spectacular / Swagger
Dev Tools	Django Admin, Git, VS Code