from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Professional
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login/customer', methods=['GET', 'POST'])
def login_customer():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email, role='Customer').first()
        if user and user.password == password:
            flash('Welcome, Customer!', category='success')
            login_user(user, remember= True)
            return redirect(url_for('custo.customer_dashboard'))
        else:
            flash('Invalid email or password', category='error')

    return render_template('customer_login.html')

@auth.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email, role='Admin').first()
        if user and user.password == password:
            flash('Welcome, Admin!', category='success')
            return redirect(url_for('adm.dashboard'))
        else:
            flash('Invalid email or password', category='error')

    return render_template('admin_login.html')

@auth.route('/login/professional', methods=['GET', 'POST'])
def login_professional():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Professional.query.filter_by(email=email, role='Professional').first()
        if user and user.password==password:
            login_user(user)
            flash('Welcome, Professional!', category='success')
            return redirect(url_for('proff.professional_dashboard'))
        else:
            flash('Invalid email or password', category='error')

    return render_template('professional_login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up')
def signup():
    return render_template("sign_up.html")

@auth.route('/customer_signup', methods = ['GET', 'POST'])
def customersignup():
    if request.method == 'POST':
        email = request.form.get('email')
        fullName = request.form.get('fullName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()
        if user:
            flash('Email already exists', category= 'error')
        elif len(email)<5:
            flash('Invalid Email', category = 'error')
        elif len(fullName)<2:
            flash('Invalid Name', category = 'error')
        elif len(password1) and len(password2) == 0:
            flash('Enter a Password', category= 'error')
        elif password1 != password2:
            flash('Password doesnt match', category='error')
        else:
            new_user = User(email = email, full_name = fullName, password = password1, role = 'Customer')
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category='success')
            return redirect(url_for('views.home'))
    return render_template("customer_signup.html")

@auth.route('/professional_signup',methods = ['GET', 'POST'])
def professionalsignup():
    if request.method == 'POST':
        email = request.form.get('email')
        fullName = request.form.get('fullName')
        ServiceName = request.form.get('ServiceName')
        Address = request.form.get('Address')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Professional.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 5:
            flash('Invalid Email', category='error')
        elif len(fullName) < 2:
            flash('Full name too short', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        else:
            new_user = Professional(
                email=email,
                full_name=fullName,
                password=password1,  
                role='Professional',
                service_name=ServiceName,
                address=Address,
                approved=False
            )
            db.session.add(new_user)
            db.session.commit()
            flash(f'You have been registered and your request is awaiting approval.', category='info')
            return redirect(url_for('auth.login'))
    
    return render_template("professional_signup.html")
