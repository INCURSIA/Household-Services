from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required,current_user
from . import db
from .models import User,Service, ServiceRequest

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")
