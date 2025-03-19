from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('main/index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html')

@bp.route('/virtual_assistant')
@login_required
def virtual_assistant():
    return render_template('main/virtual_assistant.html', message="该功能正在开发中")

@bp.route('/consultation')
@login_required
def consultation():
    return render_template('main/consultation.html', message="该功能正在开发中")

@bp.route('/financial_analysis')
@login_required
def financial_analysis():
    return render_template('main/financial_analysis.html', message="该功能正在开发中")

@bp.route('/portfolio_management')
@login_required
def portfolio_management():
    return render_template('main/portfolio_management.html', message="该功能正在开发中")
