from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Professional, ServiceRequest, Service
from datetime import datetime
from . import db
import json

custo = Blueprint('custo', __name__)

@custo.route('/customer/dashboard', methods=['GET', 'POST'])
@login_required
def customer_dashboard():
    query = request.args.get('query', '')  
    pin_code = request.args.get('pin_code', '')  
    
    services = Service.query
    if query:
        services = services.filter(Service.name.ilike(f'%{query}%'))
    if pin_code:
        services = services.filter_by(pin_code=pin_code)
    services = services.all()  # Finalize query
    requests = ServiceRequest.query.filter_by(user_email=current_user.email).all()
    requested_count = ServiceRequest.query.filter_by(user_email=current_user.email, status='Pending').count()
    assigned_count = ServiceRequest.query.filter_by(user_email=current_user.email, status='Assigned').count()
    closed_count = ServiceRequest.query.filter_by(user_email=current_user.email, status='Closed').count()

    status_data = {
        'requested': requested_count,
        'assigned': assigned_count,
        'closed': closed_count
    }

    return render_template('customer_dashboard.html', services=services, requests = requests, status_data=json.dumps(status_data))

@custo.route('/request_service/<int:service_id>', methods=['POST'])
@login_required
def request_service(service_id):
    service = Service.query.get_or_404(service_id)
    
    new_request = ServiceRequest(
        user_email=current_user.email,
        service_id=service.id,
        status='Pending',
        date_created=datetime.now()
    )
    db.session.add(new_request)
    db.session.commit()
    flash('Service request created successfully!', 'success')
    return redirect(url_for('custo.customer_dashboard'))

@custo.route('/my_requests', methods=['GET'])
@login_required
def my_requests():
    requests = ServiceRequest.query.filter_by(user_email=current_user.email).all()
    return render_template('my_requests.html', requests=requests)

@custo.route('/close_request/<int:request_id>', methods=['POST'])
@login_required
def close_request(request_id):
    request_item = ServiceRequest.query.get_or_404(request_id)
    if request_item.user_email != current_user.email:
        flash('You are not authorized to close this request.', 'danger')
        return redirect(url_for('custo.my_requests'))
    
    request_item.status = 'Closed'
    db.session.commit()
    flash('Service request closed successfully!', 'success')
    return redirect(url_for('custo.my_requests'))

@custo.route('/add_remark/<int:request_id>', methods=['POST'])
@login_required
def add_remark(request_id):
    request_item = ServiceRequest.query.get_or_404(request_id)
    if request_item.user_email != current_user.email or request_item.status != 'Closed':
        flash('Remarks can only be added to your closed requests.', 'danger')
        return redirect(url_for('custo.my_requests'))
    
    remark = request.form.get('remark')
    request_item.remarks = remark
    db.session.commit()
    flash('Remark added successfully!', 'success')
    return redirect(url_for('custo.my_requests'))

@custo.route('/edit_request/<int:request_id>', methods=['GET', 'POST'])
@login_required
def edit_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    if service_request.user_email != current_user.email:
        flash('You are not authorized to edit this request.', 'danger')
        return redirect(url_for('custo.my_requests'))
    
    if request.method == 'POST':
        remarks = request.form.get('remarks')
        service_request.remarks = remarks
        db.session.commit()
        flash('Service request updated successfully!', 'success')
        return redirect(url_for('custo.my_requests'))
    
    return render_template('edit_request.html', request=service_request)

@custo.route('/customer_profile', methods=['GET', 'POST'])
@login_required
def customer_profile():
    user = current_user  
    if request.method == 'POST':
        user.full_name = request.form.get('full_name')
        user.email = request.form.get('email')
        user.phone_number = request.form.get('phone_number')  
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('custo.customer_profile'))
    return render_template('customer_profile.html', user=user)

@custo.route('/customer_summary')
@login_required
def customer_summary():
    customer_email = current_user.email
    requested_count = ServiceRequest.query.filter_by(user_email=customer_email, status="Pending").count()
    assigned_count = ServiceRequest.query.filter_by(user_email=customer_email, status="Assigned").count()
    closed_count = ServiceRequest.query.filter_by(user_email=customer_email, status="Closed").count()
    return render_template(
        'customer_summary.html',
        requested_count=requested_count,
        assigned_count=assigned_count,
        closed_count=closed_count
    )

@custo.route('/request_service_view/<int:service_id>', methods=['GET', 'POST'])
@login_required
def request_service_view(service_id):
    service = Service.query.get_or_404(service_id) 
    professionals = Professional.query.filter_by(service_name=service.name).all()
    if request.method == 'POST':
        professional_email = request.form.get('professional_email')
        professional = Professional.query.filter_by(email=professional_email).first()

        if professional:
            new_request = ServiceRequest(
                user_email=current_user.email,
                service_id=service.id,
                professional_email=professional.email,
                status='Pending',
                date_created=datetime.now()
            )
            db.session.add(new_request)
            db.session.commit()
            flash('Service request created successfully!', 'success')
            return redirect(url_for('custo.customer_dashboard'))
        else:
            pass

    return render_template('request_service_view.html', service=service, professionals=professionals)
