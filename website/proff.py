from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Professional, ServiceRequest
from . import db

proff = Blueprint('proff', __name__)

from .models import ServiceRequest, Service, Professional

@proff.route('/professional_dashboard')
@login_required
def professional_dashboard():
    if not current_user.is_authenticated:
        flash("You must log in to access this page", "danger")
        return redirect(url_for('auth.login'))

    
    professional_service_name = current_user.service_name

    active_requests = ServiceRequest.query.join(Service).filter(
        ServiceRequest.professional_email == current_user.email,
        ServiceRequest.status == "Assigned",
        Service.name == professional_service_name  
    ).all()

    pending_requests = ServiceRequest.query.join(Service).filter(
        Service.name == professional_service_name,  
        ServiceRequest.status == "Pending"
    ).all()

    completed_requests = ServiceRequest.query.filter_by(professional_email=current_user.email, status="Closed").all()

    return render_template(
        'professional_dashboard.html', 
        pending_requests=pending_requests, 
        active_requests=active_requests, 
        completed_requests=completed_requests
    )

                        
@proff.route('/professional_summary')
@login_required
def professional_summary():
    professional_service_name = current_user.service_name

    assigned_count = ServiceRequest.query.filter_by(professional_email=current_user.email, status="Assigned").count()
    completed_count = ServiceRequest.query.filter_by(professional_email=current_user.email, status="Closed").count()
    pending_count = ServiceRequest.query.filter_by(professional_email=current_user.email, status="Pending").count()

    return render_template(
        'professional_summary.html',assigned_count=assigned_count,completed_count=completed_count,pending_count=pending_count)


@proff.route('/accept_request/<int:request_id>', methods=['POST'])
@login_required
def accept_request(request_id):
    service_request = ServiceRequest.query.get(request_id)
    if service_request:
        service_request.professional_email = current_user.email  
        service_request.status = "Assigned"  
        db.session.commit()  
        flash("Service request has been accepted!", "success")
    else:
        flash("Service request not found.", "danger")

    return redirect(url_for('proff.professional_dashboard'))


@proff.route('/reject_request/<int:request_id>', methods=['POST'])
@login_required
def reject_request(request_id):
    service_request = ServiceRequest.query.get(request_id)
    
    if service_request:
        service_request.status = "Rejected"
        db.session.commit()  
        flash("Service request has been rejected.", "danger")
    else:
        flash("Service request not found.", "danger")

    return redirect(url_for('proff.professional_dashboard'))

@proff.route('/close_request/<int:request_id>', methods=['POST'])
@login_required
def close_request(request_id):
    service_request = ServiceRequest.query.get(request_id)
    
    if service_request:
        if service_request.professional_email == current_user.email:  
            service_request.status = "Closed"  
            db.session.commit() 
            flash("Service request has been closed.", "success")
        else:
            flash("You are not authorized to close this service request.", "danger")
    else:
        flash("Service request not found.", "danger")

    return redirect(url_for('proff.professional_dashboard'))

@proff.route('/my_profile', methods=['GET', 'POST'])
@login_required
def professional_profile():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        service_name = request.form.get('service_name')
        
        professional = Professional.query.filter_by(email=current_user.email).first()
        
        if professional:
            professional.full_name = full_name
            professional.email = email
            professional.service_name = service_name
            
            db.session.commit()
            flash("Your profile has been updated successfully.", "success")
        else:
            flash("Error updating your profile.", "danger")
        return redirect(url_for('proff.professional_profile'))
    
    return render_template('professional_profile.html', professional=current_user)
