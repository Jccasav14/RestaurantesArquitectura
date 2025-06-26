# app/controllers/table_controller.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from app.services.table_service import TableService
from app.dtos.table_dto import TableDTO
from app.models.db import Restaurant

table_bp = Blueprint('table', __name__, url_prefix='/admin/tables')

def check_admin():
    if current_user.role != 'admin':
        flash('No tienes permiso para esta sección', 'error')
        return False
    return True

@table_bp.route('/restaurant/<int:restaurant_id>')
@login_required
def list_tables(restaurant_id):
    if current_user.role != 'admin':
        flash('Esta sección es solo para administradores.', 'error')
        return redirect(url_for('auth.login'))
    
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    tables = TableService.get_by_restaurant(restaurant_id)
    return render_template('admin/table_list.html', restaurant=restaurant, tables=tables)

@table_bp.route('/restaurant/<int:restaurant_id>/new', methods=['GET', 'POST'])
@login_required
def add_table(restaurant_id):
    if current_user.role != 'admin':
        flash('Esta sección es solo para administradores.', 'error')
        return redirect(url_for('auth.login'))

    restaurant = Restaurant.query.get_or_404(restaurant_id)

    if request.method == 'POST':
        number_raw = request.form.get('number', '').strip()
        type = request.form.get('type', '').strip()
        capacity_raw = request.form.get('capacity', '').strip()
        description = request.form.get('description', '').strip()

        if not number_raw or not type or not capacity_raw:
            flash('Número, tipo y capacidad son obligatorios', 'error')
            return render_template('admin/add_table.html', restaurant=restaurant)

        try:
            number = int(number_raw)
            capacity = int(capacity_raw)
        except ValueError:
            flash('Número y capacidad deben ser números válidos', 'error')
            return render_template('admin/add_table.html', restaurant=restaurant)

        dto = TableDTO(
            id=None,
            number=number,
            type=type,
            capacity=capacity,
            description=description,
            restaurant_id=restaurant.id
        )

        success = TableService.create(dto)
        if success:
            flash('Mesa creada exitosamente', 'success')
            return redirect(url_for('table.list_tables', restaurant_id=restaurant.id))
        else:
            flash('Error al crear mesa', 'error')

    return render_template('admin/add_table.html', restaurant=restaurant)

@table_bp.route('/edit/<int:table_id>', methods=['GET', 'POST'])
@login_required
def edit_table(table_id):
    if current_user.role != 'admin':
        flash('Esta sección es solo para administradores.', 'error')
        return redirect(url_for('auth.login'))

    dto = TableService.get_by_id(table_id)
    if not dto:
        flash('Mesa no encontrada', 'error')
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        number = request.form.get('number', type=int)
        type = request.form.get('type')
        capacity = request.form.get('capacity', type=int)
        description = request.form.get('description')

        if not number or not type or not capacity:
            flash('Número, tipo y capacidad son obligatorios', 'error')
            return render_template('admin/edit_table.html', table=dto)

        new_dto = TableDTO(
            id=table_id,
            number=number,
            type=type,
            capacity=capacity,
            description=description,
            restaurant_id=dto.restaurant_id
        )

        success = TableService.update(table_id, new_dto)
        if success:
            flash('Mesa actualizada exitosamente', 'success')
            return redirect(url_for('table.list_tables', restaurant_id=dto.restaurant_id))
        else:
            flash('Error al actualizar mesa', 'error')

    return render_template('admin/edit_table.html', table=dto)

@table_bp.route('/delete/<int:table_id>', methods=['POST'])
@login_required
def delete_table(table_id):
    if current_user.role != 'admin':
        flash('Esta sección es solo para administradores.', 'error')
        return redirect(url_for('auth.login'))

    dto = TableService.get_by_id(table_id)
    if not dto:
        flash('Mesa no encontrada', 'error')
        return redirect(url_for('admin.dashboard'))

    success = TableService.delete(table_id)
    if success:
        flash('Mesa eliminada exitosamente', 'success')
        return redirect(url_for('table.list_tables', restaurant_id=dto.restaurant_id))
    else:
        flash('No se pudo eliminar la mesa', 'error')
        return redirect(url_for('table.list_tables', restaurant_id=dto.restaurant_id))
