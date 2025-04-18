from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User, Service, Professional, ServiceRequest
from flask import jsonify
from . import db

adm = Blueprint('adm', __name__)

@adm.route('/dashboard')
def dashboard():
    customers = User.query.filter_by(role='Customer').all()
    professionals = Professional.query.filter_by(role='Professional',approved=True).all()
    pending_professionals = Professional.query.filter_by(approved=False).all()
    services = Service.query.all() 
    service_requests = ServiceRequest.query.all() 
    return render_template('admin_dashboard.html', customers=customers, professionals=professionals, pending_professionals=pending_professionals,services=services,service_requests=service_requests)

@adm.route('/approve_professional/<string:email>', methods=['POST'])
def approve_professional(email):
    professional = Professional.query.filter_by(email=email).first()
    if professional:
        professional.approved = True  # Set approved to True
        db.session.commit()
        flash(f'Professional  has been approved and added.', category='success')
    else:
        flash('Professional not found.', category='error')
    return redirect(url_for('adm.dashboard'))

@adm.route('/reject_professional/<string:email>', methods=['POST'])
def reject_professional(email):
    professional = Professional.query.filter_by(email=email).first()
    if professional:
        db.session.delete(professional)  # Remove from the database
        db.session.commit()
        flash(f'Professional {professional.full_name} has been rejected and removed.', category='danger')
    else:
        flash('Professional not found.', category='error')
    return redirect(url_for('adm.dashboard'))


@adm.route('/block_user/<string:email>', methods=['POST'])
def block_user(email):
    user = User.query.filter_by(email=email).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.email} has been blocked.', category='success')
    else:
        flash('User not found.', category='error')
    return redirect(url_for('adm.dashboard'))

@adm.route('/create_service', methods=['GET', 'POST'])
def create_service():
    if request.method == 'POST':
        name = request.form.get('name')
        base_price = request.form.get('base_price')
        description = request.form.get('description')
        pin_code = request.form.get('pin_code')

        if not name or not base_price:
            flash('Name and Base Price are required!', category='error')
        else:
            new_service = Service(name=name, base_price=float(base_price), description=description,pin_code=int(pin_code))
            db.session.add(new_service)
            db.session.commit()
            flash(f'Service {name} created successfully!', category='success')
            return redirect(url_for('adm.dashboard'))

    return render_template('create_service.html')

@adm.route('/update_service/<int:service_id>', methods=['GET', 'POST'])
def update_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        flash('Service not found!', category='error')
        return redirect(url_for('adm.dashboard'))

    if request.method == 'POST':
        service.name = request.form.get('name', service.name)
        service.base_price = float(request.form.get('base_price', service.base_price))
        service.description = request.form.get('description', service.description)
        service.pin_code = int(request.form.get('pin_code', service.pin_code))

        db.session.commit()
        flash(f'Service {service.name} updated successfully!', category='success')
        return redirect(url_for('adm.dashboard'))

    return render_template('update_service.html', service=service)

@adm.route('/delete_service/<int:service_id>', methods=['POST'])
def delete_service(service_id):
    service = Service.query.get(service_id)
    if service:
        db.session.delete(service)
        db.session.commit()
        flash(f'Service {service.name} has been deleted.', category='success')
    else:
        flash('Service not found.', category='error')
    return redirect(url_for('adm.dashboard'))

@adm.route('/search_professional', methods=['GET'])
def search_professional():
    query = request.args.get('query', '')
    if query:
        professionals = Professional.query.filter(
            Professional.email.ilike(f'%{query}%') | Professional.full_name.ilike(f'%{query}%')
        ).all()
        return render_template('admin_dashboard.html', search_results=professionals)
    else:
        flash('Please enter a search term.', category='error')
        return redirect(url_for('adm.dashboard'))

@adm.route('/admin_summary', methods=['GET'])
def admin_summary():
    pending = ServiceRequest.query.filter_by(status='Pending').count()
    assigned = ServiceRequest.query.filter_by(status='Assigned').count()
    closed = ServiceRequest.query.filter_by(status='Closed').count()

    service_request_data = {
        'statuses': ['Pending', 'Assigned', 'Closed'],
        'counts': [pending, assigned, closed]
    }

    return render_template('admin_summary.html', data=service_request_data)
